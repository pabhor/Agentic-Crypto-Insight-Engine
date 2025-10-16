# agents/analyzer_agent.py
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain import LLMChain, PromptTemplate
from core.config import LLM_MODEL_NAME
from loguru import logger
import json
import torch

DEFAULT_PROMPT = """
You are a financial analyst for cryptocurrencies. Given the article text, produce a JSON with keys:
- tone: short label (e.g., 'cautious optimism')
- reasoning: evidence-based reasoning with citations to article fragments (short)
- entities: list of named entities (exchanges, regulators, companies, tokens)
- implications: short market implication in 2 sentences
Return only valid JSON.
Article: {text}
"""

class AnalyzerAgent:
    def __init__(self, model_name=LLM_MODEL_NAME, device=None):
        self.model_name = model_name
        if device is None:
            self.device = 0 if torch.cuda.is_available() else -1
        else:
            self.device = device
        logger.info(f"Loading LLM {model_name} on device {self.device}")
        # lightweight pipeline: if model is instruction-tuned use text-generation
        try:
            tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
            model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32, device_map="auto" if torch.cuda.is_available() else None)
            self.pipe = pipeline("text-generation", model=model, tokenizer=tok, device=0 if torch.cuda.is_available() else -1, max_new_tokens=512)
        except Exception as e:
            logger.error(f"LLM load error: {e}. Falling back to small model.")
            # fallback to a small model for local CPU testing
            self.pipe = pipeline("text-generation", model="gpt2", max_new_tokens=128)

        self.prompt = PromptTemplate(input_variables=["text"], template=DEFAULT_PROMPT)

    def analyze(self, text: str) -> dict:
        prompt_text = self.prompt.format(text=text)
        out = self.pipe(prompt_text, do_sample=False, max_new_tokens=512)[0]["generated_text"]
        # some models echo prompt; extract JSON tail
        json_part = self._extract_json(out)
        if json_part is None:
            # Try to create minimal output
            return {
                "tone": "unknown",
                "reasoning": "Could not parse model output",
                "entities": [],
                "implications": ""
            }
        try:
            return json.loads(json_part)
        except Exception as e:
            logger.error(f"JSON parse error: {e}")
            return {"tone": "unknown", "reasoning": out[:400], "entities": [], "implications": ""}

    @staticmethod
    def _extract_json(text: str):
        # find first { and last }
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            return text[start:end]
        except ValueError:
            return None

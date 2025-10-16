# core/logger.py
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO", backtrace=False, diagnose=False)
logger.add("logs/engine_{time}.log", rotation="10 MB", level="DEBUG", backtrace=True, diagnose=True)

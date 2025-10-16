
---

# 7) Dockerfile + `docker-compose.yml` outline

**`Dockerfile`**
```Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential git && \
    pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]

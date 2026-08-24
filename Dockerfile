FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY knowledge_base/ ./knowledge_base/
COPY index/ ./index/
COPY bot.py .
COPY build_index.py .

CMD ["python", "bot.py"]
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY receipt_relay ./receipt_relay
CMD ["uvicorn", "receipt_relay.web.main:app", "--host", "0.0.0.0", "--port", "8081"]

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --default-timeout=300 --retries=10 --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn","--bind","0.0.0.0:5000","run:app"]

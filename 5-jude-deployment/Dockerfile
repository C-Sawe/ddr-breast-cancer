FROM python:3.12-slim
WORKDIR /app
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api/ api/
COPY model/*.joblib model/
ENV MODEL_DIR=/app/model PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "gunicorn -w 2 -b 0.0.0.0:${PORT} api.app:app"]

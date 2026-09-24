FROM python:3.13-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir ".[api]"

EXPOSE 8000
CMD ["uvicorn", "screenshot_action.api:app", "--host", "0.0.0.0", "--port", "8000"]

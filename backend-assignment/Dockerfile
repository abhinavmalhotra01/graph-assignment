FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["sh", "-c", "python setup_backend.py && python -m fastapi dev app/main.py --host 0.0.0.0 --port 8000"]

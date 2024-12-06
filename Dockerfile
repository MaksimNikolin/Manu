FROM python:3.12.7-slim-bookworm

WORKDIR /usr/local/webapp/

COPY . .

RUN ["pip3", "install", "--no-cache-dir", "-r", "requirements.txt"]

ENTRYPOINT ["python3", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "80", "app:asgi"]
FROM python:3.14-slim
WORKDIR /app
RUN pip install --no-cache-dir requests
ADD mensabot.py .
CMD ["python", "mensabot.py"]

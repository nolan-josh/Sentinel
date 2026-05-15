FROM python:3.12-slim

WORKDIR /app

RUN pip install pymongo

COPY scripts/listener.py .

CMD ["python", "-u", "listener.py"]

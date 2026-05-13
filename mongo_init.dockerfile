FROM python:3.12-slim

WORKDIR /app

RUN pip install pymongo

COPY scripts/mongo_init.py .

CMD ["python", "-u", "mongo_init.py"]

FROM python:3.10-slim
WORKDIR /ingestion_manager
COPY requirements.txt .

RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3", "ingestion_manager.py"]
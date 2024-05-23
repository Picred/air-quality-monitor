FROM python:3.10-slim
WORKDIR /ingestion-manager
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ingestion_manager.py .
COPY demo_data.json .

ENTRYPOINT ["python3", "ingestion_manager.py"]"
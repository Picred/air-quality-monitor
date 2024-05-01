FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ingestion_manager.py .

ENV API_KEY="0e72cb61-87b6-4ab4-b422-0886e1305ac6"
ENV COUNTRY_NAME="Italy"
ENV STATE_NAME="Sicily"
ENV GPS_LAT="37.500000"
ENV GPS_LON="15.090278"
ENV CITY_TO_SCAN="San Filippo del Mela"
ENV DATA_ACTION="NEAREST_GPS_CITY"

ENTRYPOINT ["python3", "ingestion_manager.py"]
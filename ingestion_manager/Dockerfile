# Usa l'immagine di Python 3.9 come base
FROM python:3.9-slim
WORKDIR /app
COPY ingestion_manager.py /app/

RUN pip install requests

ENV API_KEY=""
ENV COUNTRY_NAME="Italy"
ENV STATE_NAME="Sicily"
ENV GPS_LAT="37.500000"
ENV GPS_LON="15.090278"
ENV CITY_TO_SCAN="Catania"
ENV DATA_ACTION="NEAREST_IP_CITY"

CMD ["python", "ingestion_manager.py"]

# docker build . -t tap:ingestion_manager
# docker run -it --rm --hostname="ingestion_manager" --network tap -e API_KEY="0e72cb61-87b6-4ab4-b422-0886e1305ac6" tap:ingestion_manager

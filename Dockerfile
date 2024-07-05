FROM python:3.10-alpine

WORKDIR /app

RUN apk update
RUN apk upgrade
RUN pip install --upgrade pip
RUN apk add git
RUN git clone https://github.com/openskynetwork/opensky-api.git ../opensky-api

COPY . .

RUN pip install -e ../opensky-api/python

RUN apk add build-base linux-headers

RUN pip install -r requirements.txt 
RUN python3 manage.py collectstatic
RUN python3 manage.py makemigrations airplanes airports favorites flights &&\
python3 manage.py migrate &&\
python3 manage.py fill_destinations flights/db_initial/destinations_database.csv &&\
python3 manage.py fill_airports_data airports/db_initial/airports_database.csv &&\
python3 manage.py fill_airplanes airplanes/db_initial/aircrafts_database.csv

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000


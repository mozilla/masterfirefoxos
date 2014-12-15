FROM python:3.4-wheezy
RUN apt-get update && apt-get install -y libpq-dev gettext libjpeg8-dev postgresql-client

ADD . /app
WORKDIR /app

RUN ./bin/peep.py install -r requirements.txt

EXPOSE 80

CMD ["./bin/run-docker.sh"]

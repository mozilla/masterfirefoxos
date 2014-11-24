FROM debian
RUN apt-get update && apt-get install -y python python-pip python-dev libpq-dev gettext libjpeg8-dev

ADD . /app
WORKDIR /app

RUN ./bin/peep.py install -r requirements.txt

EXPOSE 80

CMD ["./bin/run-docker.sh"]

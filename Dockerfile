FROM python:3.4-wheezy
RUN apt-get update && apt-get install -y libpq-dev gettext libjpeg8-dev postgresql-client

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
ADD ./bin/peep.py /app/bin/peep.py
RUN ./bin/peep.py install -r requirements.txt

ADD . /app
COPY ./.git/HEAD /app/masterfirefoxos/base/static/revision.txt

EXPOSE 80

CMD ["./bin/run-docker.sh"]

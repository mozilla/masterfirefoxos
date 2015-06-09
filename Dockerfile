FROM python:3.3-slim

EXPOSE 80
CMD ["./bin/run-docker.sh"]

RUN apt-get update &&\
    apt-get install -y --no-install-recommends build-essential python-dev libpq-dev gettext libjpeg62-turbo-dev postgresql-client sharutils &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./bin/peep.py /app/bin/peep.py
RUN ./bin/peep.py install -r requirements.txt

ADD https://github.com/mozilla/masterfirefoxos-l10n/archive/master.tar.gz /tmp/locale.tar.gz
RUN mkdir -p /app/locale && tar zxf /tmp/locale.tar.gz -C /app/locale --strip-components 1
COPY . /app

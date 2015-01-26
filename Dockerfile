FROM python:3.4-wheezy
RUN apt-get update &&\
    apt-get install -y --no-install-recommends libpq-dev gettext libjpeg8-dev postgresql-client &&\
    apt-get remove mysql-common -y && apt-get autoremove -y &&\
    apt-get upgrade -y

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./bin/peep.py /app/bin/peep.py
RUN ./bin/peep.py install -r requirements.txt

ADD https://github.com/mozilla/masterfirefoxos-l10n/archive/master.tar.gz /tmp/locale.tar.gz
RUN mkdir -p /app/locale && tar zxf /tmp/locale.tar.gz -C /app/locale --strip-components 1
COPY . /app
COPY ./.git/HEAD /app/masterfirefoxos/base/static/revision.txt

EXPOSE 80

CMD ["./bin/run-docker.sh"]

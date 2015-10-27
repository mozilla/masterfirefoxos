FROM debian:jessie
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

EXPOSE 8000
CMD ["./bin/run-docker.sh"]

RUN adduser --uid 1000 --disabled-password --gecos '' --no-create-home webdev

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3 python3-dev python3-pip libpq-dev gettext libjpeg62-turbo-dev postgresql-client sharutils libjpeg62-turbo
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

# Pin a known to work with peep pip version.
RUN pip install pip==6.0.0

# Install app
COPY ./requirements.txt /app/requirements.txt
COPY ./bin/peep.py /app/bin/peep.py
RUN ./bin/peep.py install --no-cache-dir -r requirements.txt

ADD https://github.com/mozilla/masterfirefoxos-l10n/archive/master.tar.gz /tmp/locale.tar.gz
RUN mkdir -p /app/locale && tar zxf /tmp/locale.tar.gz -C /app/locale --strip-components 1
COPY . /app

# Cleanup
RUN apt-get purge -y python-dev build-essential libpq-dev libjpeg62-turbo-dev
RUN apt-get autoremove -y
RUN rm -rf /var/lib/{apt,dpkg,cache,log} /usr/share/doc /usr/share/man /tmp/*

# Change User
RUN chown webdev.webdev -R .
USER webdev

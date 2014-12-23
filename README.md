masterfirefoxos
===============

The Master Firefox OS Website https://wiki.mozilla.org/Websites/Master_Firefox_OS

[![Docs Status](https://readthedocs.org/projects/masterfirefoxos/badge/?version=latest&style=)](http://masterfirefoxos.mozilla.org/)
[![Build Status](https://ci.masterfirefoxos.com/job/mozilla_masterfirefoxos/badge/icon)](https://ci.masterfirefoxos.com/job/mozilla_masterfirefoxos/)
[![Requirements Status](https://requires.io/github/mozilla/masterfirefoxos/requirements.svg?branch=master)](https://requires.io/github/mozilla/masterfirefoxos/requirements/?branch=master)

Docs
----

Documentation can be found at http://masterfirefoxos.rtfd.org/.


Building Documentation Locally
------------------------------
The instructions below assume you have Python and
[pip](https://pip.pypa.io/) installed. It is also
strongly recommended that you create and activate a
[virtualenv](https://virtualenv.pypa.io/) first.

If you'd like to build the documentation locally:

```sh
   pip install -r requirements.txt
   cd docs
   make html
```

The resulting docs can be located under the ``_build/html`` directory.

You can also run ``make livehtml`` to launch a webserver on
http://127.0.0.1:8000 that auto-rebuild the documentation when any files are
changed.

Docker for development
----------------------

0. Make sure you have [docker](https://docker.io) and [fig](https://pypi.python.org/pypi/fig)
1. fig up

Note that this will probably not work with
[boot2docker](https://github.com/boot2docker/boot2docker), as the
volumes will not get mounted.


Docker for deploying to production
-----------------------------------

1. Add your project in [Docker Registry](https://registry.hub.docker.com/) as [Automated Build](http://docs.docker.com/docker-hub/builds/)
2. Prepare a 'env' file with all the variables needed by dev, stage or production.
3. Run the image:

    docker run --env-file env -p 80:80 mozilla/masterfirefoxos


NewRelic Monitoring
-------------------

A newrelic.ini file is already included. To enable NewRelic monitoring
add two enviroment variables:

 - NEW_RELIC_LICENSE_KEY
 - NEW_RELIC_APP_NAME

See the [full list of supported environment variables](https://docs.newrelic.com/docs/agents/python-agent/installation-configuration/python-agent-configuration#environment-variables).

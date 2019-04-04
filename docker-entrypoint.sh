#!/bin/bash

# Initialize SECRET_KEY for Django if none is already given
local_settings="./server/local_settings.py"
if ! grep 'SECRET_KEY' "${local_settings}" &> /dev/null ; then
    echo "SECRET_KEY = 'supersecretkey'" >> "${local_settings}"
fi

# Only allow localhost, because used behind a proxy
echo "ALLOWED_HOSTS = ['127.0.0.1']" >> "${local_settings}"

if [[ ! -z "${DEMO+x}" ]]; then
    echo "DEMO = ${DEMO}" >> "${local_settings}"
fi

if [[ ! -z "${LANGUAGE_CODE+x}" ]]; then
    echo "LANGUAGE_CODE = '${LANGUAGE_CODE}'" >> "${local_settings}"
fi

if [[ ! -z "${TIME_ZONE+x}" ]]; then
    echo "TIME_ZONE = '${TIME_ZONE}'" >> "${local_settings}"
fi

# Prepare database migration
python3 ./manage.py migrate

# Load sample data into database
if [[ ! -z "${FIXTURE+x}" ]]; then
    python3 ./manage.py loaddata "${FIXTURE}"
else
    echo "Fixture is not set, skipping loading fixtures…"
fi

# Compile translations
python3 ./manage.py compilemessages

# Collect static files
python3 ./manage.py compilescss
python3 ./manage.py collectstatic --ignore=*.scss

# Run webserver
uwsgi --ini uwsgi.ini
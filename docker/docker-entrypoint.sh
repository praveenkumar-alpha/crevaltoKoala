#!/bin/sh

local_settings_file="./server/local_settings.py"
uwsgi_file="docker/uwsgi.ini"

echo "# This file is generated automatically, do not edit manually" > "${local_settings_file}"
echo "SECRET_KEY = '$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)'" >> "${local_settings_file}"
echo "ALLOWED_HOSTS = ['localhost', '127.0.0.1']" >> "${local_settings_file}"

if [[ ! -z "${DEBUG+x}" ]]; then
    echo "DEBUG = True" >> "${local_settings_file}"
fi

if [[ ! -z "${DEMO+x}" ]]; then
    echo "DEMO = True" >> "${local_settings_file}"
fi

if [[ ! -z "${LANGUAGE_CODE+x}" ]]; then
    echo "LANGUAGE_CODE = '${LANGUAGE_CODE}'" >> "${local_settings_file}"
fi

if [[ ! -z "${TIME_ZONE+x}" ]]; then
    echo "TIME_ZONE = '${TIME_ZONE}'" >> "${local_settings_file}"
fi

if [[ "$(id -u)" -ne 0 ]]; then
    echo "uid=$(id -u)" >> "${uwsgi_file}"
    echo "gid=$(id -g)" >> "${uwsgi_file}"
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
python3 ./manage.py collectstatic --ignore=*.scss

# Run webserver
uwsgi --ini "${uwsgi_file}"

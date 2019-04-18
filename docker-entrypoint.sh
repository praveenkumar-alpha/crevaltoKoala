#!/bin/sh

local_settings_file="./server/local_settings.py"
echo "# This file is generated automatically, do not edit manually"

# Initialize django secret key
if ! grep 'SECRET_KEY' "${local_settings_file}" &> /dev/null ; then
    echo "SECRET_KEY = '$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)'" >> "${local_settings_file}"
fi

# Only allow localhost, because used behind a proxy
echo "ALLOWED_HOSTS = ['127.0.0.1', 'localhost']" >> "${local_settings_file}"

# If running in demo (variable should exists, whatever it contains), install dependencies from current build
if [[ ! -z "${DEMO+x}" ]]; then
    echo "DEMO = True" >> "${local_settings_file}"
    curl -L "https://gitlab.com/koala-lms/django-learning/-/jobs/artifacts/master/download?job=package" -o learning.zip
    mkdir learning && unzip -o learning.zip -d ./learning && pip install learning/dist/*.tar.gz && rm -rf learning
fi

if [[ ! -z "${LANGUAGE_CODE+x}" ]]; then
    echo "LANGUAGE_CODE = '${LANGUAGE_CODE}'" >> "${local_settings_file}"
fi

if [[ ! -z "${TIME_ZONE+x}" ]]; then
    echo "TIME_ZONE = '${TIME_ZONE}'" >> "${local_settings_file}"
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
uwsgi --ini uwsgi.ini

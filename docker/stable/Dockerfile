FROM python:alpine
LABEL maintainer="Guillaume Bernard <gbernard@koala-lms.org>"

# Implicitely creates directory
WORKDIR /koala_lms

# It will be possible to access the webserver from port 8080
EXPOSE 8080

# Allow the end user to run the container as another user. User is uwsgi
ENV USER=uwsgi

# Add Koala-LMS code to workdir
ADD [".", "."]

RUN apk add --no-cache gettext build-base zlib-dev jpeg-dev linux-headers musl-dev mariadb-connector-c mariadb-connector-c-dev && \
    # Install Python requirements
    pip3 install --no-cache-dir -r requirements.txt uwsgi mysqlclient && \
    # Remove unused dependencies
    apk del build-base zlib-dev linux-headers musl-dev mariadb-connector-c-dev && \
    # Create the user that will be able to run the container
    addgroup -S "${USER}" && adduser -S "${USER}" -G "${USER}" && chown "${USER}":"${USER}" -R . && \
    # Give execution right to entrypoint
    chmod u+x docker/docker-entrypoint.sh

ENTRYPOINT ["/bin/sh", "./docker/docker-entrypoint.sh"]

USER "${USER}"

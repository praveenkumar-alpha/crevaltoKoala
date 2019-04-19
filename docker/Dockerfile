FROM python:alpine
LABEL maintainer="Guillaume Bernard <gbernard@koala-lms.org>"

# Let this first for caching reasons
RUN apk add --no-cache gettext build-base zlib-dev jpeg-dev linux-headers musl-dev

# Implicitely creates directory
WORKDIR /koala_lms

# Add Koala-LMS code to workdir
ADD [".", "."]

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt uwsgi

# Create the user that will run the application and transfer property
RUN chmod u+x ./docker/docker-entrypoint.sh

# It will be possible to access the webserver from port 8080
EXPOSE 8080

# Allow the end user to run the container as another user. This is not forced by default
ENV USER=uwsgi
RUN addgroup -S "${USER}" && adduser -S "${USER}" -G "${USER}" && chown "${USER}":"${USER}" -R .

# Remove unecessary packages
RUN apk del build-base zlib-dev linux-headers musl-dev

ENTRYPOINT ["/bin/sh", "./docker/docker-entrypoint.sh"]

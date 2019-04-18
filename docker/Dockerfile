FROM python:alpine
LABEL maintainer="Guillaume Bernard <gbernard@koala-lms.org>"

# Let this first for caching reasons
RUN apk add --no-cache gettext build-base unzip zlib-dev jpeg-dev curl linux-headers musl-dev

# Implicitely creates directory
WORKDIR /koala_lms

# Add Koala-LMS code to workdir
ADD [".", "."]

# Install requirements
RUN pip3 install -r requirements.txt uwsgi

# Create the user that will run the application and transfer property
RUN chmod u+x ./docker/docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "./docker/docker-entrypoint.sh"]

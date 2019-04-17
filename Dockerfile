FROM python:alpine
MAINTAINER Guillaume Bernard <gbernard@koala-lms.org>

# Let this first for caching reasons
RUN apk add --no-cache gettext build-base unzip zlib-dev jpeg-dev curl linux-headers musl-dev

# Implicitely creates directory
WORKDIR /koala_lms
ADD requirements.txt /koala_lms/requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt uwsgi

# Add LMS code
ADD .  /koala_lms/

# Create the user that will run the application and transfer property
RUN addgroup -S demo && adduser -S demo -G demo && chown demo:demo -R .
RUN chmod u+x /koala_lms/docker-entrypoint.sh

# Remove unused packages
RUN apk del build-base linux-headers musl-dev zlib-dev

USER demo
ENTRYPOINT docker-entrypoint.sh

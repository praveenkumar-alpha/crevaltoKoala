FROM python:slim
MAINTAINER Guillaume Bernard <gbernard@koala-lms.org>

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Let this first for caching reasons
RUN apt update && \
    apt install -y gettext intltool gnome-doc-utils itstool libmariadbclient-dev libicu-dev build-essential git unzip

# Implicitely creates directory
WORKDIR /koala_lms
COPY requirements.txt /koala_lms/requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt uwsgi
COPY .  /koala_lms/

RUN chmod u+x /koala_lms/docker-entrypoint.sh
ENTRYPOINT docker-entrypoint.sh

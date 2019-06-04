FROM registry.gitlab.com/koala-lms/lms:latest
LABEL maintainer="Guillaume Bernard <gbernard@koala-lms.org>"

# Add Koala-LMS code to workdir
ADD [".", "."]

USER root

RUN \
    # Install Koala-LMS official applications manually
    sh docker/devel/django-accounts.sh && \
    sh docker/devel/django-learning.sh && \
    # Change owner of Koala-LMS files
    chown ${USER}:${USER} -R .

USER "${USER}"

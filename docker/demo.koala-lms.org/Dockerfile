FROM registry.gitlab.com/koala-lms/lms:latest

RUN apk add --no-cache curl build-base zlib-dev linux-headers musl-dev unzip && \
    curl -L "https://gitlab.com/koala-lms/django-learning/-/jobs/artifacts/master/download?job=package" -o learning.zip && \
    mkdir learning && unzip -o learning.zip -d ./learning && pip install --no-cache-dir learning/dist/*.tar.gz && rm -rf learning && rm learning.zip && \
    apk del curl build-base zlib-dev linux-headers musl-dev unzip

USER "${USER}"

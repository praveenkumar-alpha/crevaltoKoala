FROM registry.gitlab.com/koala-lms/lms:latest

RUN curl -L "https://gitlab.com/koala-lms/django-learning/-/jobs/artifacts/master/download?job=package" -o learning.zip && \
    mkdir learning && unzip -o learning.zip -d ./learning && pip install learning/dist/*.tar.gz && rm -rf learning

RUN addgroup -S demo && adduser -S demo -G demo && chown demo:demo -R .
USER demo
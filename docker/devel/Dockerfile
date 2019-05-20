FROM registry.gitlab.com/koala-lms/lms:latest

RUN apk add --no-cache curl build-base zlib-dev linux-headers musl-dev unzip && \
    for project in "django-learning" "django-accounts"; do \
        curl -L "https://gitlab.com/koala-lms/${project}/-/jobs/artifacts/develop/download?job=package" -o "${project}".zip && \
        mkdir "${project}" && unzip -o "${project}".zip -d ./"${project}" && pip install --no-cache-dir "${project}"/dist/*.tar.gz && rm -rf "${project}" && rm "${project}".zip; \
    done && \
    apk del curl build-base zlib-dev linux-headers musl-dev unzip

USER "${USER}"

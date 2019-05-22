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

RUN apk add --no-cache curl build-base zlib-dev jpeg-dev linux-headers musl-dev git sassc mariadb-connector-c-dev mariadb-connector-c gettext && \
    # Install Python requirements
    pip3 install --no-cache-dir -r requirements.txt uwsgi mysqlclient && \
    # Make entrypoint executable
    chmod u+x ./docker/docker-entrypoint.sh && \
    # Install projects
    for project in "django-learning" "django-accounts"; do \
        # Clone repository and switch to develop branch
        git clone "https://gitlab.com/koala-lms/${project}.git" "${project}" && cd "${project}" && git checkout develop && \
        # Compile PO files
        django-admin compilemessages && \
        # Compile SCSS files
        if find -name scss -type d | egrep '.*'; then \
            cd -- "$(find -name scss -type d -print0)" && for file in *.scss; do sassc ${file} `basename ${file} .scss`.css; done \
        fi && \
        # Make package
        cd /koala_lms/${project} && python3 setup.py sdist bdist_wheel &> /dev/null && \
        # Install package
        pip install --no-deps --force-reinstall dist/*.tar.gz && \
        # Remove build artifacts and source code
        cd .. && rm -rf "${project}"; \
    done && \
    apk del curl build-base zlib-dev linux-headers musl-dev mariadb-connector-c-dev git sassc && \
    # Create the user that will be able to run the container
    addgroup -S "${USER}" && adduser -S "${USER}" -G "${USER}" && chown "${USER}":"${USER}" -R .

USER "${USER}"

ENTRYPOINT ["/bin/sh", "./docker/docker-entrypoint.sh"]

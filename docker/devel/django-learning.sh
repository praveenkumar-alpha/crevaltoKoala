#!/usr/bin/env sh

export BASE_DIR="${PWD}"
export APPLICATION="django-learning"
export DJANGO_LEARNING_URL="https://gitlab.com/koala-lms/${APPLICATION}.git"
export DJANGO_LEARNING_REQUIREMENTS="jpeg-dev gettext"
export DJANGO_LEARNING_BUILD_REQUIREMENTS="build-base zlib-dev git sassc"

# Install Alpine requirements
apk add --no-cache ${DJANGO_LEARNING_REQUIREMENTS} ${DJANGO_LEARNING_BUILD_REQUIREMENTS} && \

# Clone django-koalalms-learning
git clone "${DJANGO_LEARNING_URL}" "${APPLICATION}" && git -C "${APPLICATION}" checkout develop && \

# Move to the folder
cd "${APPLICATION}" && \

# Install Python requirements
pip3 install --no-cache-dir -r requirements.txt && \

# Compile translations
django-admin compilemessages && \

# Compile stylesheet
sassc "learning/static/learning/scss/learning.scss" "learning/static/learning/scss/learning.css" && \

# Build the Python package
python3 setup.py sdist bdist_wheel > /dev/null && \

# Install the package in the system
pip install --no-deps --force-reinstall dist/*.tar.gz && \

# Remove build artifacts and source code
cd "${BASE_DIR}" && rm -rf "${APPLICATION}" && \

# Remove unnecessary packages
apk del ${DJANGO_LEARNING_BUILD_REQUIREMENTS}

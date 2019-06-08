#!/usr/bin/env sh

export BASE_DIR="${PWD}"
export APPLICATION="django-accounts"
export DJANGO_ACCOUNTS_URL="https://gitlab.com/koala-lms/${APPLICATION}.git"
export DJANGO_ACCOUNTS_REQUIREMENTS="gettext"
export DJANGO_ACCOUNTS_BUILD_REQUIREMENTS="git"

# Install Alpine requirements
apk add --no-cache ${DJANGO_ACCOUNTS_REQUIREMENTS} ${DJANGO_ACCOUNTS_BUILD_REQUIREMENTS} && \

# Clone django-koalalms-accounts
git clone "${DJANGO_ACCOUNTS_URL}" "${APPLICATION}" && git -C "${APPLICATION}" checkout develop && \

# Move to the folder
cd "${APPLICATION}" && \

# Install Python requirements
pip3 install --no-cache-dir -r requirements.txt && \

# Compile translations
django-admin compilemessages && \

# Build the Python package
python3 setup.py sdist bdist_wheel > /dev/null && \

# Install the package in the system
pip install --no-deps --force-reinstall dist/*.tar.gz && \

# Remove build artifacts and source code
cd "${BASE_DIR}" && rm -rf "${APPLICATION}" && \

# Remove unnecessary packages
apk del ${DJANGO_ACCOUNTS_BUILD_REQUIREMENTS}

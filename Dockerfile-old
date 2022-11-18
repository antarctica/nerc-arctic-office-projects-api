FROM python:3.6-alpine3.12

LABEL maintainer = "Web & Apps team <webapps@bas.ac.uk>"

# Setup project
WORKDIR /usr/src/app

ENV PYTHONPATH /usr/src/app
ENV FLASK_APP manage.py
ENV FLASK_ENV development

# Setup project dependencies
COPY requirements.txt /usr/src/app/
RUN apk add --no-cache postgresql-libs libffi-dev libressl-dev python3-dev py-pip && \
    apk add --no-cache --virtual .build-deps build-base linux-headers postgresql-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# Setup runtime
ENTRYPOINT []

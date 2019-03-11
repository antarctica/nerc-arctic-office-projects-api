FROM python:3.6-alpine

LABEL maintainer = "Felix Fennell <felnne@bas.ac.uk>"

# Setup project
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app
RUN apk add --no-cache build-base linux-headers libffi-dev openssl-dev python3-dev py-pip && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del build-base linux-headers

ENTRYPOINT [ "python" ]
CMD [ "sample-client.py" ]

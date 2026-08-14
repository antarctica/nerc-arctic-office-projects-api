FROM python:3.12-alpine AS base

LABEL maintainer="BAS Web Apps <webapps@bas.ac.uk>"

RUN apk add --no-cache \
    libxslt-dev \
    libffi-dev \
    openssl-dev \
    libxml2-utils \
    postgresql-dev \
    build-base \
    cargo

FROM base AS run

WORKDIR /usr/src/app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT=/venv
ENV PATH="/venv/bin:$PATH"

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --locked --no-dev

COPY . .

ENTRYPOINT []
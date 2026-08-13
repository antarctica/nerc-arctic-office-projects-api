FROM python:3.12-alpine AS base

LABEL maintainer = "BAS Web Apps <webapps@bas.ac.uk>"

RUN apk add --no-cache \
    libxslt-dev \
    libffi-dev \
    openssl-dev \
    libxml2-utils \
    postgresql-dev

FROM base AS poetry

RUN apk add --no-cache build-base cargo
RUN python3 -m pip install pipx
RUN python3 -m pipx install poetry==2.4.1

FROM poetry AS run

WORKDIR /usr/src/app

ENV POETRY_VIRTUALENVS_PATH=/venv
ENV PATH="/venv/bin:/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry install --no-interaction --no-ansi
RUN poetry run python -m pip install --upgrade pip

RUN poetry env info
RUN poetry run python -c "import sys; print(sys.executable)"
RUN poetry run python -m pip show arctic-office-projects-api || true
RUN poetry run python -c "import importlib.metadata; print([x.metadata['Name'] for x in importlib.metadata.distributions() if 'arctic' in x.metadata['Name'].lower()])"

ENTRYPOINT []
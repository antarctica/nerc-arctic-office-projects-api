#!/usr/bin/env ash -e -x

# install dependencies
poetry install
# migrate database
poetry run flask db upgrade;
# import static data
poetry run flask import categories resources/science-categories.json;
poetry run flask import organisations resources/funder-organisations.json;
poetry run flask import organisations resources/people-organisations.json;

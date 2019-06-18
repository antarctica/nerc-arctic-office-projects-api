#!/usr/bin/env ash -e -x

# migrate database
flask db upgrade;
# import static data
flask import categories resources/science-categories.json;
flask import organisations resources/funder-organisations.json;
flask import organisations resources/people-organisations.json;

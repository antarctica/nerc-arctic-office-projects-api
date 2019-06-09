#!/usr/bin/env ash -e -x

# migrate database
flask db upgrade;
# import static data
flask import categories resources/science-categories.json;

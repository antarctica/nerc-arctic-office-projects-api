#!/usr/bin/env ash -e -x

# migrate database
flask db upgrade;

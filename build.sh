#!/usr/bin/env bash
set -o errexit

# Install system dependencies for psycopg2
apt-get update
apt-get install -y libpq-dev

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Django setup
python manage.py collectstatic --no-input
python manage.py migrate

#!/usr/bin/env bash
export WITH_TRACER=true
export TRACER_HOST=localhost
export TRACER_PORT=5775
export TRACER_TOKEN=123
export FLASK_SUPPORT=true
export TOKEN=123
export SERVICE_NAME=template_api
export REALM=template_api
export DB_HOSTS='postgresql://postgres:senha#123@localhost:5435/postgres'

gunicorn --bind 0.0.0.0:8000 --reuse-port wsgi:application
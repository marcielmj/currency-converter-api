#!/bin/sh

gunicorn --bind=0.0.0.0 -k uvicorn.workers.UvicornWorker --timeout 600 --chdir src/currency_converter_api main:app

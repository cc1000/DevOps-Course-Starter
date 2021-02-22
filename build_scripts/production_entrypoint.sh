#!/bin/bash
poetry run gunicorn -b 0.0.0.0:$PORT --chdir /src wsgi
FROM python:3.8.6-buster as base
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
EXPOSE 5000
COPY poetry.toml /
COPY poetry.lock pyproject.toml /

FROM base as production
COPY /src/templates/ /src/templates/
COPY /src/*.py /src/
RUN poetry install --no-dev --no-root
ENTRYPOINT poetry run gunicorn -b 0.0.0.0:5000 --chdir /src wsgi

FROM base as development
ENV FLASK_ENV=development
RUN poetry install --no-root
# Relies on root source directory being mounted to /src
ENTRYPOINT poetry run flask run --host=0.0.0.0
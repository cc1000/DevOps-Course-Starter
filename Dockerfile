FROM python:3.8.6-buster as base
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
EXPOSE 5000
COPY poetry.toml /
COPY poetry.lock pyproject.toml /

FROM base as production
ENTRYPOINT poetry run gunicorn -b 0.0.0.0:5000 --chdir /src wsgi
RUN poetry install --no-dev --no-root
COPY /src/templates/ /src/templates/
COPY /src/*.py /src/

FROM base as development
ENV FLASK_ENV=development
# Relies on root source directory being mounted to /src
ENTRYPOINT poetry run flask run --host=0.0.0.0
RUN poetry install --no-root

FROM base as test
ENTRYPOINT ["poetry", "run", "pytest"]
RUN poetry install --no-root
COPY /src/templates/ /src/templates/
COPY /src/*.py /src/
COPY /src/tests/*.py /src/tests/
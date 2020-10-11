FROM python:3.8.6-buster as base
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
EXPOSE 5000

FROM base as production
COPY poetry.toml /
COPY poetry.lock pyproject.toml /
COPY templates /templates/
COPY *.py /
RUN poetry install --no-dev --no-root
RUN ls -la
ENTRYPOINT poetry run gunicorn -b 0.0.0.0:5000 wsgi

FROM base as development
ENV FLASK_ENV=development
COPY / .
RUN poetry install --no-root
RUN ls -la
ENTRYPOINT poetry run flask run --host=0.0.0.0
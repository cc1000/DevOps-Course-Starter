FROM python:3.8.6-buster
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
EXPOSE 5000
COPY poetry.toml /
COPY poetry.lock pyproject.toml /
COPY templates /templates/
COPY *.py /
RUN poetry install --no-dev --no-root
ENTRYPOINT poetry run gunicorn -b 0.0.0.0:5000 wsgi
#####
# BASE
#####
FROM python:3.8.6-buster as base
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
EXPOSE 5000
COPY poetry.toml /
COPY poetry.lock pyproject.toml /


#####
# PRODUCTION
#####
FROM base as production
ENTRYPOINT poetry run gunicorn -b 0.0.0.0:${PORT} --chdir /src wsgi
EXPOSE ${PORT}
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-root
COPY /src/templates/ /src/templates/
COPY /src/*.py /src/

#####
# DEVELOPMENT
#####
FROM base as development
ENV FLASK_ENV=development
# Relies on root source directory being mounted to /src
ENTRYPOINT poetry run flask run --host=0.0.0.0
RUN poetry install --no-root

#####
# TESTS
#####
FROM base as test

# Install Chrome
RUN echo "Installing Chrome" &&\
 curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
 apt-get update &&\
 apt-get install ./chrome.deb -y &&\
 rm ./chrome.deb

# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
 echo "Installing Chromium WebDriver version ${LATEST}" &&\
 curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
 apt-get install unzip -y &&\
 unzip ./chromedriver_linux64.zip

ENTRYPOINT ["poetry", "run", "pytest"]

RUN poetry install --no-root
COPY /src/templates/ /src/templates/
COPY /src/*.py /src/
COPY /src/tests/*.py /src/tests/
COPY /src/tests_e2e/*.py /src/tests_e2e/
# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Mongo Atlas config
To run the application you will need to add the following config to your local .env file:
* MONGO_URI: URI of Mongo cluster (eg cluster0.hxawy.mongodb.net)
* MONGO_USERNAME: Username for connecting to Mongo cluster/DB (retrieve from https://cloud.mongodb.com/v2/6049be1a61f4334ef8e891c7#security/database/users)
* MONGO_PASSWORD: Password for Mongo user
* MONGO_DB_NAME: Name of Mongo DB to use (eg todo_app)

## Setup for Selenium E2E tests
* Download the Chrome WebDriver
    * Details [here](https://chromedriver.chromium.org/home) (you can get the latest version number [here](https://chromedriver.storage.googleapis.com/LATEST_RELEASE))
    * Extract zip contents (chromedriver.exe) to root project directory
    * Ensure Chrome is installed
* To use Firefox instead of Chrome
    * Download the Gecko WebDriver exe from [here](https://github.com/mozilla/geckodriver/releases/latest)
    * Extract zip contents (geckodriver.exe) to root project directory
    * Ensure Firefox is installed
    * Change E2E tests to use Firefox as driver: ```with webdriver.Firefox() as driver```

## Running tests
In a terminal, run:
* Integration tests: ```src/pytest tests```
* E2E tests: ```pytest src/tests_e2e```

## Running in a Vagrant VM
* Install hypervisor (eg Windows Hyper-V or Oracle VirtualBox)
* Install Vagrant
* In a terminal in root of project, run: ```vagrant up```

## Docker
Run ```docker-compose up -d --build``` (or ```docker-compose -f docker-compose.prod.yml up -d --build``` for prod).
### Running tests in Docker image
* To build test target, run: ```docker build --target test --tag todo-app-test .```
* To execute tests in container, run:
    * Unit/integration: ```docker run --env-file ./.env.test todo-app-test src/tests```
    * E2E: ``` docker run --env-file "./.env.test_e2e" -e MONGO_URI=[INSERT VALUE] -e MONGO_USERNAME=[INSERT VALUE] MONGO_PASSWORD=[INSERT VALUE] todo-app-test "src/tests_e2e"```

## Travis CI build
### Secrets
Sensitive environment variables (eg Mongo settings) need to be set as variables in repository settings in Travis. 

An alternative is to encrypt the environment variables and include in .travis.yml. However, I couldn't get this working using the Windows Ruby CLI tool. 

Reference for both approaches [here](https://docs.travis-ci.com/user/environment-variables).
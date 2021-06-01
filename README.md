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

## MongoDB
To run the application you will need to add the following config to your local .env file:
* MONGO_CONNECTION_STRING: Connection string to Mongo cluster (see below)
* MONGO_DB_NAME: Name of Mongo DB to use (eg todo_app)

### Atlas
To point to a cloud-hosted Atlas cluster, set the connection string to ```mongodb+srv://<username>:<password>@cluster0.hxawy.mongodb.net```. User details can be fetched from [here](https://cloud.mongodb.com/v2/6049be1a61f4334ef8e891c7#security/database/users).

## Authentication
To authenticate you will need a GitHub account. For development, you will need to set the following environment variables from a GitHub account set up with OAuth linked to http://localhost:5000: ```OAUTH_CLIENT_ID```, ```OAUTH_CLIENT_SECRET```. Call back route needs to be ```/login/callback```.

Authentication can be disabled by setting the environment variable ```AUTHENTICATION_DISABLED``` to false. 

## Authorisation
ATOW, users are hardcoded in ```AuthProvider``` (pending completion of module 10 stretch goals!). For now simply add your GitHub username here to access the app. 

### Local Docker
To run Mongo in a local Docker container run ```docker run --name local-mongo -v <local data path>:/data/db -p 27017:27017 -d mongo:4.4.4-bionic```. Set ```local data path``` to a directory on your host machine for storing Mongo data (optional as the base image sets up a volume by default; see [here](https://hub.docker.com/_/mongo)).

Set the connection string to ```mongodb://localhost```. 

Alternatively just run the default docker-compose file as this will create the MongoDB container and override the connection string automatically.

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
    * E2E: ``` docker run --env-file "./.env.test_e2e" -e MONGO_CONNECTION_STRING=[INSERT VALUE] todo-app-test "src/tests_e2e"```

## Travis CI build
https://travis-ci.com/github/cc1000/DevOps-Course-Starter

### Secrets
Sensitive environment variables (eg Mongo settings) need to be set as variables in repository settings in Travis. 

An alternative is to encrypt the environment variables and include in .travis.yml. However, I couldn't get this working using the Windows Ruby CLI tool. 

Reference for both approaches [here](https://docs.travis-ci.com/user/environment-variables).

## Provisioning infrastructure
Can be spun up using Terraform, as per ```.\main.tf```, using ```terraform apply```. Use ```terraform plan``` to see what actions it will perform. 

To prevent inputting environment variables each time when running ```apply``` locally, create file ```.\terraform.tfvars``` and run ```terraform apply -var-file="terraform.tfvars"```.

### State back-end
State is stored in Azure Storage. You need to set the access key for the storage account used to environment variable ```ARM_ACCESS_KEY```.

### Travis CI integration
Add environment variable ```TF_VERSION=0.14.7```.

The following environment variables are also needed to allow the CI server (eg Travis) to authenticate with Azure Storage: ```ARM_CLIENT_ID```, ```ARM_TENANT_ID```, ```ARM_SUBSCRIPTION_ID```, ```ARM_CLIENT_SECRET```. These come from the Service Principal created for CI.
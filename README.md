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

## Trello config
To run the application you will need to add the following config to your local .env file:
* TRELLO_ROOT_URL: Trello API URL (eg https://api.trello.com/1)
* TRELLO_API_KEY: Trello API key
* TRELLO_TOKEN: Tello user token generated with access to the board
* TRELLO_BOARD_NAME: NAme of Trello board to use for the app

## Running Selenium E2E tests
Download the Gecko Driver exe from [here](https://github.com/mozilla/geckodriver/releases/latest) and extract exe to root project directory. 
# Toy PO (Purchase Order) App

This is a toy PO (purchase order) app, written with FastAPI.
It is an end-to-end app using sqlite3 as its backend. ORM Models
are written with SQLAlchemy, and we also leverage Pydantic models
with FastAPI for automatic schema validation and autogenerated
OpenAPI documentation.

## Requirements

Only tested with Python 3.11 on ubuntu.

## Setup

We use pipenv to install dependencies (and also to run
developer workflow tasks, mentioned later). Poetry would
probably be a great option but I haven't gotten a chance to 
work with it yet.

Create a `.env` file, because this app is env-var configurable:
```
envsubst < ..env.example > .env
```

And install dependencies using pipenv:
```
pipenv install --dev
```

## Development

We store our development workflow tasks in our Pipfile. See
the `[scripts]` section of the Pipfile if you'd like to
run commands directly. You can always activate the Pipenv
virtual environment and shell and run the command yourself,
if desired:

```bash
# Example of using autopep8 directly
pipenv shell
# wait until shell is loaded, then run
autopep8 --in-place --recursive toypo
```

For ease of use though, here are the predetermined
developer workflow tasks:

* ```
  pipenv run app
  ```
  Start a local webserver on port 8000
* ```
  pipenv run autoformat
  ```
  Run autopep8 autoformatter
* ```
  pipenv run lint
  ```
  Run pylint
* ```
  pipenv run test
  ```
  Run unit tests. A sqlite3 test DB file is created temporarily,
  but should be removed when tests are completed.

## RESTful API Documentation

To view autogenerated documentation, start the app
and then go to http://localhost:8000/docs. You'll see
operations such as `GET /purchase_orders/` all listed
out there.

FastAPI builds and serves these OpenAPI docs as a
first-class feature of the service, and documentation
is shown by default. This works well for internal services,
but external services would require better authentication.
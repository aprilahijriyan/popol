# Popol API

Demo API

## Installation

Since this project depends on the latest version of "popol", you can use the virtual environment created by `python-poetry` in the parent directory.

```sh
cd ..
poetry shell
cd examples
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Copy env file:

```sh
cp .env.example .env
```

## Usage

Run docker services:

```sh
docker-compose up
```

Run database migration:

```sh
alembic stamp head
alembic upgrade head
```

Run the SMTP server:

```sh
python -m smtpd -c DebuggingServer -n -d
```

Run SAQ Worker:

```sh
popol saq runworker --queue default
```

Run the application:

```sh
uvicorn app.main:app --reload
```

## Development

Install dependencies:

```sh
pip install -r requirements-dev.txt
```

Setup pre-commit hooks:

```sh
pre-commit install
```

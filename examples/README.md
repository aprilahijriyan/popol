# Popol API

Demo API

## Installation

Setup virtual environment:

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## Usage

Run docker services:

```
docker-compose up
```

Run database migration:

```
alembic stamp head
alembic upgrade head
```

Run the SMTP server:

```
python -m smtpd -c DebuggingServer -n -d
```

Run SAQ Worker:

```
popol saq runworker --queue default
```

Run the application:

```
uvicorn app.main:app --reload
```

## Development

Install dependencies:

```
pip install -r requirements-dev.txt
```

Setup pre-commit hooks:

```
pre-commit install
```

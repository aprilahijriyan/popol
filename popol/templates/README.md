# {{ project_name }}

{{ project_description }}

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

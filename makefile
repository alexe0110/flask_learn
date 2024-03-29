VENV ?= .venv
PYTHON_VERSION := 3.11

init:
	python$(PYTHON_VERSION) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

test:
	pytest -s --alluredir=/tmp/allure --clean-alluredir

test-cov:
	pytest --cov=application --cov-report=html

run:
	docker-compose build
	docker-compose up -d
	$(VENV)/bin/alembic upgrade head
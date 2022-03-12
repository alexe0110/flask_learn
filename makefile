VENV ?= .venv
PYTHON_VERSION := 3.9

init:
	python$(PYTHON_VERSION) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

test:
	pytest -s --alluredir=/tmp/allure --clean-alluredir

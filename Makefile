VENV ?= venv
PY := $(VENV)/bin/python

.PHONY: install lint format check

install:
	uv venv --python 3.8 $(VENV)
	uv pip install --python $(PY) --build-constraint build-constraints.txt -r requirements-dev.txt

lint:
	$(VENV)/bin/ruff check .

format:
	$(VENV)/bin/ruff format .
	$(VENV)/bin/ruff check --fix .

check: lint
	$(VENV)/bin/ruff format --check .

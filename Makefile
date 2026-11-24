.PHONY: clean isort isort-check format format-check fix lint type-check pytest check test documentation


init:
	poetry install

clean:
	rm -rf .coverage .hypothesis .mypy_cache .pytest_cache .tox *.egg-info
	rm -rf dist
	find . | grep -E "(__pycache__|docs_.*$$|\.pyc|\.pyo$$)" | xargs rm -rf

isort:
	isort .

isort-check:
	isort . --check-only --diff

format:
	black .

format-check:
	black --check --diff .

fix: isort format

lint:
	flake8 --exclude=.tox,build

type-check:
	mypy --pretty src tests

check: lint isort-check format-check type-check

pytest:
	pytest

test: check pytest


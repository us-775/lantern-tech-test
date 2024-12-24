install:
		poetry install --no-root

dev:
	  poetry run fastapi dev src/main.py

test:
	  poetry run python -m unittest discover tests

.PHONY: install dev

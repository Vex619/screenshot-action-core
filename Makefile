.PHONY: test lint evaluate build

test:
	python -m pytest -q

lint:
	ruff check .

evaluate:
	python scripts_evaluate.py

build:
	python -m build

.PHONY: diagram install lint format-check type-check ci venv

PROJECTS = diagrams
VENV = .venv

venv:
	@if [ ! -d "$(VENV)" ]; then \
		uv venv; \
	fi

diagram:
	uv run --with diagrams python diagrams/system_diagram.py

install: venv
	uv pip install --python $(VENV)/bin/python -r requirements.txt

lint:
	uvx ruff check .

format-check:
	uvx ruff format --check --diff .

type-check:
	@for project in $(PROJECTS); do \
		echo "Running type check for $$project..."; \
		cd $$project && uv sync --dev && uvx ty check && cd ..; \
	done

ci: lint format-check type-check
	@echo "All CI checks passed"


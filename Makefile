.PHONY: diagram install lint format-check type-check ci

PROJECTS = diagrams

diagram:
	uv run --with diagrams python diagrams/system_diagram.py

install:
	uv pip install -r requirements.txt

lint:
	ruff check .

format-check:
	ruff format --check --diff .

type-check:
	@for project in $(PROJECTS); do \
		echo "Running type check for $$project..."; \
		cd $$project && uv sync --dev && uvx ty check && cd ..; \
	done

ci: lint format-check type-check
	@echo "All CI checks passed"


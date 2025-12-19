.PHONY: diagram install lint format-check type-check ci

# プロジェクトのリスト
PROJECTS = diagrams

# 図を生成
diagram:
	uv run --with diagrams python diagrams/system_diagram.py

# 依存関係をインストール
install:
	uv pip install -r requirements.txt

# Lintチェック
lint:
	ruff check .

# フォーマットチェック
format-check:
	ruff format --check --diff .

# 型チェック
type-check:
	@for project in $(PROJECTS); do \
		echo "Running type check for $$project..."; \
		cd $$project && uv sync --dev && uvx ty check && cd ..; \
	done

# CI相当のすべてのチェックを実行
ci: lint format-check type-check
	@echo "All CI checks passed"


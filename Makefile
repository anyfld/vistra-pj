.PHONY: diagram install

# 図を生成
diagram:
	uv run --with diagrams python diagrams/system_diagram.py

# 依存関係をインストール
install:
	uv pip install -r requirements.txt


# Makefile

test-cov:
    pytest --cov=src --cov-report=html --cov-report=term

lint:
    uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/
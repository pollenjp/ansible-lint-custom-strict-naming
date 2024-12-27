
.PHONY: test
test:
	rm -rf .venv
	uv cache clean ansible-lint-custom-strict-naming
	uv run ansible-lint

.PHONY: install
install:
	rm -rf .venv
	uv sync


.PHONY: debug
debug:
	${MAKE} install
#	uv run ansible-lint -vvv
	uv run ansible-lint

.PHONY: install
install:
	rm -rf .venv
	uv sync

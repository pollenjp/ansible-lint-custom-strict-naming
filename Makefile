
.PHONY: lint
lint:
	uv run ruff check
	uv run pyright

.PHONY: fmt
fmt:
	uv run ruff format

.PHONY: build
build:
	${MAKE} clean
	uvx --from build pyproject-build --installer uv

.PHONY: clean
clean:
	rm -rf build dist *.egg-info

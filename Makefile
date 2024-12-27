
.PHONY: lint
lint:
	uv run ruff check
	uv run pyright

.PHONY: fmt
fmt:
	uv run ruff format

.PHONY: test
test:
	uv run pytest
	${MAKE} -C ./examples/sample1 test

.PHONY: clean
clean:
	rm -rf build dist *.egg-info

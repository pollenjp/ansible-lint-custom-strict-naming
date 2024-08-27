
.PHONY: lint
lint:
	rye run ruff check
	rye run pyright

.PHONY: fmt
fmt:
	rye run ruff format

.PHONY: test
test:
	rye run nox -s test

.PHONY: nox
nox:
	rye run nox

.PHONY: build
build:
	${MAKE} clean
	rye build

.PHONY: clean
clean:
	rm -rf dist *.egg-info

publish-test:
	${MAKE} build
	rye publish --verbose --repository testpypi --repository-url https://test.pypi.org/legacy/


publish-prod:
	${MAKE} build
	rye publish

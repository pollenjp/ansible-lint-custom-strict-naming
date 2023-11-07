
.PHONY: lint
lint:
	rye run nox -s lint

.PHONY: format
format:
	rye run nox -s format

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
	rm -rf build dist *.egg-info

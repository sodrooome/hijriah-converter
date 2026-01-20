.PHONY: test coverage clean build

PYTHON := python3

# run all the tests without coverage
test:
	$(PYTHON) -m unittest discover .

coverage:
	coverage run -m unittest discover .
	coverage report -m

clean:
	rm -rf build *.egg-info dist

build: clean
	$(PYTHON) -m build

publish-test: build
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish-prod: build
	$(PYTHON) -m twine upload dist/*

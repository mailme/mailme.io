.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "devinstall - install all packages required for development"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "docs - generate Sphinx HTML documentation, including API docs"

clean: clean-build clean-pyc

devinstall:
	pip install -e .[tox]
	pip install -e .[docs]
	pip install -e .[tests]

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 mailme tests

test:
	py.test tests/ -v --cov mailme --cov-report term-missing

test-all:
	tox

docs:
	rm -f docs/mailme.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ mailme
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

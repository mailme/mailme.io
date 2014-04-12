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

develop:
	npm install
	pip install -e . --allow-all-external
	pip install "file://`pwd`#egg=mailme[tox]"
	pip install "file://`pwd`#egg=mailme[docs]"
	pip install "file://`pwd`#egg=mailme[tests]"
	bower update
	gem install -g Gemfile --no-rdoc --no-ri

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 mailme --ignore='E122,E124,E125,E126,E128,E501,F403' --exclude="**/migrations/**"

test-ci:
	$(MAKE) test

test:
	py.test tests/ -vs --cov mailme --cov-report term-missing --pep8 --flakes

test-all:
	tox

docs:
	rm -f docs/mailme.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ mailme
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

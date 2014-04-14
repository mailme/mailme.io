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

docs: clean-build
	sphinx-apidoc --force -o docs/modules/ mailme mailme/*/migrations
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

clean-build:
	rm -fr build/ src/build
	rm -fr dist/ src/dist
	rm -fr *.egg-info src/*.egg-info
	rm -fr htmlcov/
	$(MAKE) -C docs clean

lint:
	flake8 mailme --ignore='E122,E124,E125,E126,E128,E501,F403' --exclude="**/migrations/**"

test-ci:
	$(MAKE) test

test:
	py.test mailme/tests/ -vs --cov mailme --cov-report term-missing --pep8 --flakes

test-all:
	tox

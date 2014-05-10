.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "develop - install all packages required for development"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "docs - generate Sphinx HTML documentation, including API docs"

clean: clean-build clean-pyc

deps:
	# for python 3.4 required right now unfortunately.
	pip install --upgrade -r requirements.txt
	pip install -e . --allow-all-external
	pip install "file://`pwd`#egg=doit[tox]"
	pip install "file://`pwd`#egg=doit[docs]"
	pip install "file://`pwd`#egg=doit[tests]"
	pip install "file://`pwd`#egg=doit[postgres]"

develop: deps
	npm install
	bower update
	gem install foreman compass

docs: clean-build
	sphinx-apidoc --force -o docs/source/modules/ src/doit src/doit/*/migrations src/doit/tests
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

clean-build:
	rm -fr build/ src/build
	rm -fr dist/ src/dist
	rm -fr *.egg-info src/*.egg-info
	rm -fr htmlcov/
	$(MAKE) -C docs clean

lint:
	flake8 doit --ignore='E122,E124,E125,E126,E128,E501,F403' --exclude="**/migrations/**"

test-ci:
	$(MAKE) test

test:
	py.test -vs --pep8 --flakes

test-coverage:
	py.test -vs --pep8 --flakes --cov doit --cov-report term-missing

test-all:
	tox

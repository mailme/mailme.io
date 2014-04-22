#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


with open('README.rst') as fobj:
    readme = fobj.read()

with open('CHANGES') as fobj:
    history = fobj.read()
    history.replace('.. :changelog:', '')


test_requires = [
    'tox',
    'py',
    'pyflakes',
    'coverage',
    'pytest',
    'pytest-cache==1.0',
    'pytest-cov>=1.4',
    'pytest-flakes',
    'pytest-pep8',
    'pytest-django',
    'factory-boy==2.3.1',
    'python-coveralls',
    'cov-core==1.7',
    'coverage==3.7.1',
    'execnet==1.1',
    'mock==1.0.1',
    'pep8==1.4.6',
    'httpretty==0.6.5',
]


install_requires = [
    'Django==1.7b2',
    'south>=0.8.4',
    'celery>=3.1',
    'django-celery>=3.1',
    'feedparser',
    'html5lib',
    'requests',
    'python-social-auth',
    'lxml',
    'pytz==2014.2',
    'django-suit',
    'blessings',
    'raven',
    'textblob',
    'python-dateutil',
    'beautifulsoup4',
    'listparser',
]


dev_requires = [
    'ipdb'
]

docs_requires = [
    'sphinx',
    'sphinx_rtd_theme'
]

postgres_requires = [
    'psycopg2>=2.5.0,<2.6.0',
]


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='mailme',
    version='0.1.0',
    description='subscribe your life!',
    long_description=readme + '\n\n' + history,
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    url='https://bitbucket.org/fruitywinter/mailme.io',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    tests_require=test_requires,
    install_requires=install_requires,
    cmdclass={'test': PyTest},
    extras_require={
        'docs': docs_requires,
        'tests': test_requires,
        'dev': dev_requires,
        'postgres': install_requires + postgres_requires,
    },
    zip_safe=False,
    license='BSD',
    classifiers=[
        '__DO NOT UPLOAD__',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)

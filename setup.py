#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


with open('README.rst') as fobj:
    readme = fobj.read()

with open('CHANGES') as fobj:
    history = fobj.read()
    history.replace('.. :changelog:', '')


dependency_links = [
    'http://nltk.org/nltk3-alpha/nltk-3.0a3.tar.gz#egg=nltk-3.0a3',
]


test_requires = [
    'coverage',
    'pytest',
    'pytest-cov>=1.4',
    'pytest-django',
    'python-coveralls',
]

install_requires = [
    'Django>=1.6,<1.7',
    'celery>=3.1',
    'django-celery>=3.1',
    'feedparser',
    'html5lib',
    'requests',
    'python-social-auth',
    'lxml',
    'pytz==2013d',
    'South',
    'django-suit',
    'blessings',
    'raven',
    'nltk<=3.0a4',
    'python-dateutil',
    'beautifulsoup4',
]

dev_requires = [
    'flake8>=2.0',
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
    description='subscribe your live!',
    long_description=readme + '\n\n' + history,
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    url='https://bitbucket.org/fruitywinter/mailme.io',
    packages=[
        'mailme',
    ],
    package_dir={'mailme': 'mailme'},
    include_package_data=True,
    tests_require=test_requires,
    install_requires=install_requires,
    cmdclass={'test': PyTest},
    dependency_links=dependency_links,
    extras_require={
        'docs': ['sphinx'],
        'tox': ['tox'],
        'tests': test_requires,
        'dev': dev_requires,
        'postgres': install_requires + postgres_requires,
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)

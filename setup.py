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
    'tox>=1.7.1,<1.8',
    'py>=1.4.20,<1.5',
    'pyflakes>=0.8.1,<0.9',
    'coverage>=3.7.1,<3.8',
    'pytest>=2.5.2,<2.6',
    'pytest-cache>=1.0,<2.0',
    'pytest-cov>=1.6,<1.7',
    'pytest-flakes>=0.2,<1.0',
    'pytest-pep8>=1.0.5,<1.1',
    'pytest-django>=2.6.1,<2.7',
    'factory-boy>=2.3.1,<2.4',
    'python-coveralls>=2.4.2,<2.5',
    'cov-core>=1.7,<1.8',
    'coverage>=3.7.1,<3.8',
    'execnet>=1.2.0,<1.3',
    'mock>=1.0.1,<1.1',
    'pep8>=1.4.6,<1.5',
    'httpretty>=0.8.0',
]


install_requires = [
    'Django>=1.7b4',
    'celery>=3.1,<3.2',
    'django-celery>=3.1,<3.2',
    'feedparser>=5.1.3,<5.2',
    'html5lib>=0.999,<1.0',
    'requests>=2.2.1,<2.3',
    'python-social-auth>=0.1.23,<0.2',
    'lxml>=3.3.5,<3.4',
    'pytz==2014.2',
    'django-suit>=0.2.8,<0.3',
    'blessings>=1.5.1,<1.6',
    'raven>=4.2.1,<4.3',
    'textblob>=0.8.4,<0.9',
    'python-dateutil>=2.2,<2.3',
    'beautifulsoup4>=4.3.2,<4.4',
    'listparser>=0.17,<0.18',

    # For Python 3.4 compatibility
    'billiard>=3.3.0.17,<3.3.1',
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

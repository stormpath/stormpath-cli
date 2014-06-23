#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

from codecs import open
from os import system
from os.path import dirname, join
from re import M, search
from subprocess import call
from sys import argv, exit, version_info

from setuptools import Command, find_packages, setup


PY_VERSION = version_info[:2]
VERSION = '0.0.1'


if argv[-1] == 'publish':
    system('python setup.py sdist upload')
    exit()


class BaseCommand(Command):
    """A generic setup.py command."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class TestDepCommand(BaseCommand):
    """Install all test dependencies."""

    description = 'install test dependencies'

    def run(self):
        cmd = ['pip', 'install', 'tox', 'pytest', 'pytest-cov']

        if PY_VERSION >= (3, 2):
            cmd.append('mock')

        exit(call(cmd))


def read(*parts):
    path = join(dirname(__file__), *parts)
    with open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = search(r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file, M)
    if version_match:
        return version_match.group(1)
    eaise RuntimeError("Unable to find version string.")

setup(
    name='stormpath-cli',
    version=find_version("stormpath_cli", "__init__.py"),
    author='Stormpath Inc.',
    author_email='python@stormpath.com',
    description='Official command line interface for the Stormpath REST API',
    url='https://github.com/stormpath/stormpath-cli',
    packages=find_packages(),
    include_package_data=True,
    keywords=['stormpath', 'client', 'cli'],
    license='Apache 2.0',
    install_requires=['docopt >= 0.6.1', 'stormpath >= 1.2.3'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Console',
        'Intended Audience :: Developers',
    ],
    cmdclass={
        'testdep': TestDepCommand,
    },
    entry_points={
        'console_scripts': [
            'stormpath = stormpath_cli.main:main'
        ]
    },
)

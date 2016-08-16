#!/usr/bin/env python
# -*- coding: utf-8 -*-


from subprocess import call
from sys import version_info

from setuptools import Command, find_packages, setup
from stormpath_cli import __version__ as version


PY_VERSION = version_info[:2]


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run the tests."""
        raise SystemExit(call(['py.test']))


setup(

    # Basic package information:
    name = 'stormpath-cli',
    version = version,
    description = 'Official command line interface for Stormpath.',
    url = 'https://github.com/stormpath/stormpath-cli',
    packages = find_packages(),
    include_package_data = True,

    # Author information:
    author = 'Stormpath Inc.',
    author_email = 'python@stormpath.com',

    # Metadata:
    keywords = ['stormpath', 'client', 'cli', 'security', 'authentication'],
    license = 'Apache 2.0',
    install_requires = [
        'docopt>=0.6.1',
        'pyquery>=1.2.13',
        'requests>=2.10.0',
        'stormpath>=1.2.4',
        'termcolor>=1.1.0',
    ],
    extras_require = {
        'test': ['codacy-coverage', 'mock', 'python-coveralls', 'pytest', 'pytest-cov', 'sphinx'],
    },
    classifiers = [
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

    # Script information:
    cmdclass = {'test': RunTests},
    entry_points = {
        'console_scripts': [
            'stormpath = stormpath_cli.main:main'
        ]
    },

)

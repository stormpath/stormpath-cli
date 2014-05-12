#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 - 2014 Stormpath, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import unicode_literals
from __future__ import absolute_import
from setuptools import setup, find_packages
import sys
import re
import os
import codecs


VERSION = '0.0.1'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

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
    install_requires=['docopt >= 0.6.1', 'stormpath >= 1.1.0'],
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
    entry_points={
        'console_scripts': [
            'stormpath = stormpath_cli.main:main'
        ]
    },
)

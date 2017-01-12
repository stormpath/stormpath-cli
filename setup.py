from subprocess import call
from sys import exit

from setuptools import Command, find_packages, setup

from stormpath_cli import __version__ as version


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
        exit(call(['py.test', '--quiet', '--cov-report=term-missing', '--cov', 'stormpath_cli']))


setup(

    # Basic package information:
    name = 'stormpath-cli',
    version = version,
    description = 'Official command line interface for Stormpath.',
    url = 'https://github.com/stormpath/stormpath-cli',
    packages = find_packages(),
    include_package_data = True,

    # Author information:
    author = 'Randall Degges',
    author_email = 'randall@stormpath.com',

    # Metadata:
    keywords = ['stormpath', 'client', 'cli', 'security', 'authentication', 'authorization'],
    license = 'Apache 2.0',
    install_requires = [
        'docopt>=0.6.2',
        'pyquery>=1.2.17',
        'requests>=2.12.4',
        'stormpath>=2.5.1',
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
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

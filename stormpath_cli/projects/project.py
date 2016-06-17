from glob import glob
from os import chdir
from subprocess import call

from termcolor import colored

from ..util import which


class Project(object):
    download_args = ['git', 'clone']
    install_args = ['npm', 'install']
    run_args = ['node', 'server.js']

    def __init__(self, remote_location, name=None):
        self.remote_location = remote_location

        if name is not None:
            self.name = name

    def download(self):
        if not which('git'):
            print(colored('\nERROR: It looks like you don\'t have the Git CLI installed, please set this up first.\n', 'red'))
            exit(1)

        if self.name:
            call(self.download_args + [self.remote_location, self.name])
        else:
            call(self.download_args + [self.remote_location])
            self.name = self.remote_location.split('.')[-2].split('/')[-1]

    def install(self):
        if not which(self.install_args[0]):
            print(colored('\nERROR: It looks like you don\'t have {} installed, please set this up first.\n'.format(self.install_args[0]), 'red'))
            exit(1)

        chdir(self.name)
        call(self.install_args)
        chdir('..')

    def run(self):
        if not which(self.run_args[0]):
            print(colored('\nERROR: It looks like you don\'t have {} installed, please set this up first.\n'.format(self.run_args[0]), 'red'))
            exit(1)

        call(self.run_args)

    @classmethod
    def create_from_type(cls, type, name=None):
        from .java import JavaProject
        from .node import NodeProject
        from .php import PHPProject
        from .ruby import RubyProject
        from .python import PythonProject
        #from .dotnet import DotNetProject

        lookup_dict = {
            'express': {
                'cls': NodeProject,
                'remote_location': 'https://github.com/stormpath/express-stormpath-sample-project.git',
            },
            'spring-boot': {
                'cls': JavaProject,
                'remote_location': 'https://github.com/stormpath/stormpath-sdk-java.git',
                'target_folder_name': 'spring-boot',
            },
            'spring-boot-webmvc': {
                'cls': JavaProject,
                'remote_location': 'https://github.com/stormpath/stormpath-sdk-java.git',
                'target_folder_name': 'spring-boot-webmvc',
            },
            'ruby': {
                'cls': RubyProject,
                'remote_location': 'https://github.com/stormpath/stormpath-heroku-ruby-sample.git',
            },
            'laravel': {
                'cls': PHPProject,
                'remote_location': 'https://github.com/stormpath/stormpath-laravel-example.git',
            },
            'flask': {
                'cls': PythonProject,
                'remote_location': 'https://github.com/stormpath/stormpath-flask-sample.git',
            },
            'django': {
                'cls': PythonProject,
                'remote_location': 'https://github.com/stormpath/stormpath-django-sample.git',
            },
            'passport': {
                'cls': NodeProject,
                'remote_location': 'https://github.com/stormpath/stormpath-passport-express-sample.git',
            }
        }

        if lookup_dict[type.lower()]['cls'] == JavaProject:
            return lookup_dict[type.lower()]['cls'](
                name = name,
                remote_location = lookup_dict[type.lower()]['remote_location'],
                target_folder_name = lookup_dict[type.lower()]['target_folder_name']
            )

        return lookup_dict[type.lower()]['cls'](name=name, remote_location=lookup_dict[type.lower()]['remote_location'])

    @classmethod
    def detect(cls):
        from .java import JavaProject
        from .node import NodeProject
        from .php import PHPProject
        from .ruby import RubyProject
        from .python import PythonProject
        #from .dotnet import DotNetProject

        files = glob('*')

        if 'pom.xml' in files:
            return JavaProject('dummy', 'dummy', 'dummy')

        if 'composer.json' in files:
            return PHPProject('dummy', 'dummy')

        if 'setup.py' in files or 'requirements.txt' in files:
            return PythonProject('dummy', 'dummy')

        if 'Gemfile' in files:
            return RubyProject('dummy', 'dummy')

        #if 'dotnet?' in files:
        #    return DotNetProject()

        if 'package.json' in files:
            return NodeProject('dummy', 'dummy')

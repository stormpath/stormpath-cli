from glob import glob
from os import chdir
from subprocess import call


class Project(object):
    download_args = ['git', 'clone']
    install_args = ['npm', 'install']
    run_args = ['node', 'server.js']

    def __init__(self, remote_location, name=None):
        self.remote_location = remote_location

        if name is not None:
            self.name = name

    def download(self):
        if self.name:
            call(self.download_args + [self.remote_location, self.name])
        else:
            call(self.download_args + [self.remote_location])
            self.name = self.remote_location.split('.')[-2].split('/')[-1]

    def install(self):
        chdir(self.name)
        call(self.install_args)
        chdir('..')

    def run(self):
        call(self.run_args)

    @classmethod
    def create_from_type(cls, type, name=None):
        from .java import JavaProject
        from .node import NodeProject
        #from .php import PHPProject
        #from .ruby import RubyProject
        #from .dotnet import DotNetProject

        lookup_dict = {
            'node': {
                'cls': NodeProject,
                'name': 'stormpath-node-sample',
                'remote_location': 'https://github.com/stormpath/stormpath-sdk-node.git',
            },
            'express': {
                'cls': NodeProject,
                'name': 'stormpath-express-sample',
                'remote_location': 'https://github.com/stormpath/express-stormpath-sample-project.git',
            },
            'spring-boot': {
                'cls': JavaProject,
                'name': 'stormpath-spring-boot-sample',
                'remote_location': 'https://github.com/stormpath/stormpath-sdk-java.git',
                'target_folder_name': 'spring-boot-default',
            },
            'spring-boot-webmvc': {
                'cls': JavaProject,
                'name': 'stormpath-spring-boot-webvc-sample',
                'remote_location': 'https://github.com/stormpath/stormpath-sdk-java.git',
                'target_folder_name': 'spring-boot-webmvc',
            },
            #'spring-security-spring-boot-webmvc': {},
            #'spring': {},
            #'spring-webmvc': {},
            #'spring-security-webmvc': {},
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
        #from .php import PHPProject
        #from .ruby import RubyProject
        #from .dotnet import DotNetProject

        files = glob('*')

        if 'pom.xml' in files:
            return JavaProject()

        #if 'composer.json' in files:
        #    return PHPProject()

        #if 'setup.py' in files:
        #    return PythonProject()

        #if 'Gemfile' in files:
        #    return RubyProject()

        #if 'dotnet?' in files:
        #    return DotNetProject()

        if 'package.json' in files:
            return NodeProject()

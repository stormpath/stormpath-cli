from subprocess import call

from termcolor import colored

from ..util import which
from .project import Project


class PHPProject(Project):
    install_args = ['composer', 'install']
    run_args = ['php', '-S', 'localhost:8080', '-t', 'public']

    def install(self):
        super(PHPProject, self).install()
        call(['cp', '{}/.env.example'.format(self.name), '{}/.env'.format(self.name)])

    def run(self):
        if not which('php'):
            print(colored('\nERROR: It looks like you don\'t have PHP insalled.  Please set this up first.\n', 'red'))
            exit(1)

        call(['php', 'artisan', 'key:generate'])
        super(PHPProject, self).run()

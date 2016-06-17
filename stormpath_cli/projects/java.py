from os import chdir
from subprocess import call, check_output

from project import Project


class JavaProject(Project):
    install_args = ['mvn', 'clean', 'install', '-Dmaven.test.skip=true']
    run_args = ['java', '-jar', 'target/*.jar']

    def __init__(self, remote_location, target_folder_name, name=None):
        self.remote_location = remote_location
        self.target_folder_name = target_folder_name

        if name is not None:
            self.name = name

    def download(self):
        self.name = 'stormpath-{}-sample'.format(self.target_folder_name)
        temp_folder = "__stormpath-cli-java-temp"

        call(self.download_args + [self.remote_location, temp_folder])

        chdir(temp_folder)
        tags = check_output(['git', 'for-each-ref', '--sort=taggerdate', '--format', '%(refname)', '%(taggerdate)', 'refs/tags'])
        tags = [line for line in tags.split('\n')]
        latest_tag = tags[len(tags) - 2]

        call(['git', 'checkout', latest_tag])
        chdir('..')

        call(['mkdir', self.name])
        call(['cp', '-R', '{}/examples/{}/'.format(temp_folder, self.target_folder_name), self.name])

        call(['rm', '-rf', temp_folder])

        chdir(self.name)
        call(['git', 'init'])
        call(['git', 'add', '--all'])
        call(['git', 'commit', '-m', 'First commit!'])
        chdir('..')

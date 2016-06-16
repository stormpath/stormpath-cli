from os import chdir
from subprocess import call, check_output

from project import Project


class JavaProject(Project):
    target_folder_name = "spring-boot-default"
    name = 'stormpath-java-sample'
    remote_location = 'https://github.com/stormpath/stormpath-sdk-java.git'
    download_args = ['git', 'clone']
    install_args = ['mvn', 'clean', 'install', '-Dmaven.test.skip=true']
    run_args = ['java', '-jar', 'target/*.jar']
    deploy_args = []

    def download(self):
        # We're going to use a temp file to keep all the java sdk files while we create sample app directory
        # it'll get cleanuped before we're done
        temp_folder = "__stormpath-cli-java-temp"

        # download the Java sdk with it's examples into the temp folder
        call(self.download_args + [self.remote_location, temp_folder])

        # make sure we're working off the latest tagged release so that the maven build later will work
        chdir(temp_folder)
        call(['ls'])
        tags = check_output(['git', 'for-each-ref', '--sort=taggerdate', '--format', '%(refname)', '%(taggerdate)', 'refs/tags'])
        tags = [line for line in tags.split('\n')]
        latest_tag = tags[len(tags) - 2]

        call(['git', 'checkout', latest_tag])
        chdir('..')

        # move the sample the intended folder the user will be using
        call(['mkdir', self.name])
        call(['cp', '-R', '{}/examples/{}/'.format(temp_folder, self.target_folder_name), self.name])

        # clean up the temp files
        call(['rm', '-rf', temp_folder])

        # prep the new sample project folder for git
        chdir(self.name)
        call(['git', 'init'])
        call(['git', 'commit', '--all'])
        chdir('..')

from project import *

class JavaProject(Project):
    target_folder_name = "spring-boot-default"
    name = 'stormpath-java-sample'
    remote_location = 'https://github.com/stormpath/stormpath-sdk-java.git'
    download_args = ['git', 'clone']
    install_args = ['mvn', 'clean', 'install', '-Dmaven.test.skip=true']
    run_args = ['java', '-jar', 'target/*.jar']
    deploy_args = []

    def download(self):
        
        #We're going to use a temp file to keep all the java sdk files while we create sample app directory
        #it'll get cleanuped before we're done
        temp_folder = "__stormpath-cli-java-temp"

        #download the Java sdk with it's examples into the temp folder
        subprocess.call(self.download_args + [self.remote_location, temp_folder])

        #make sure we're working off the latest tagged release so that the maven build later will work
        os.chdir(temp_folder)
        subprocess.call(['ls'])
        tags = subprocess.check_output(['git', 'for-each-ref', '--sort=taggerdate', '--format', '%(refname)', '%(taggerdate)', 'refs/tags'])
        tags = [line for line in tags.split('\n')]
        latest_tag = tags[len(tags) - 2]

        subprocess.call(['git', 'checkout', latest_tag])
        os.chdir('..')
        
        #move the sample the intended folder the user will be using    
        subprocess.call(['mkdir', self.name])
        subprocess.call(['cp', '-R', '%s/examples/%s/'%(temp_folder, self.target_folder_name), self.name])

        #clean up the temp files
        subprocess.call(['rm', '-rf', temp_folder])

        #prep the new sample project folder for git
        os.chdir(self.name)
        subprocess.call(['git', 'init'])
        subprocess.call(['git', 'commit', '--all'])
        os.chdir('..')

    #end download


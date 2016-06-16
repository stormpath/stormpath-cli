import subprocess
import os

class Project(object):

    name = 'stormpath-sample'
    remote_location = 'https://github.com/stormpath/express-stormpath-sample-project.git'
    download_args = ['git', 'clone']
    install_args = ['npm', 'install']
    run_args = ['node', 'server.js']
    deploy_args = []


    def __init__(self, name=None, remote_location=None, ):
        if name is not None:
            self.name = name

        if remote_location is not None:
            self.remote_location = remote_location        

    def download(self):
        if self.name is not None and self.name is not '':
            subprocess.call(self.download_args + [self.remote_location, self.name])
        else:
            subprocess.call(self.download_args + [self.remote_location])

    #end download

    def install(self,args=None):
        """gonna test it within the folder"""
        #print("folder:%s  cmd: %s"% (self.name, self.install_args + args if args else self.install_args))
        os.chdir(self.name)
        subprocess.call(self.install_args + args if args else self.install_args)
        os.chdir('..')

    def run(self, project_name=None):
        """if theres no project name than run within the folder you're in"""
        subprocess.call(self.run_args)

    def deploy(self):
        subprocess.call(self.deploy_args)

    @classmethod
    def lookup(klass, name):
        lookup_dict = {
            'express':{
                cls:NodejsProject, 
                name:'stormpath-express-sample', 
                remote_location:'https://github.com/stormpath/express-stormpath-sample-project.git',
            },
            'spring-boot' :{
                cls:JavaProject,
                name:'stormpath-spring-boot-sample', 
                remote_location:'https://github.com/stormpath/stormpath-sdk-java.git',
                target_folder_name : "spring-boot-default",
            },
            'spring-boot-webmvc' :{
                cls:JavaProject,
                name:'stormpath-spring-boot-webvc-sample', 
                remote_location:'https://github.com/stormpath/stormpath-sdk-java.git',
                target_folder_name:"spring-boot-webmvc",
            },
            'spring-security-spring-boot-webmvc': {},
            'spring':{},
            'spring-webmvc':{},
            'spring-security-webmvc':{},
        }
        return klass(...)

    @classmethod 
    def detect():
        return JavaProject


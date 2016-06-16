from project import *

class NodeProject(Project):

    name = 'stormpath-nodejs-sample'
    remote_location = 'https://github.com/stormpath/express-stormpath-sample-project.git'
    download_args = ['git', 'clone']
    install_args = ['npm', 'install']
    run_args = ['node', 'server.js']
    deploy_args = []

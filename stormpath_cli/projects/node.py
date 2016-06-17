from project import Project


class NodeProject(Project):
    install_args = ['npm', 'install']
    run_args = ['npm', 'start']

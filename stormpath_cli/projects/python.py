from project import Project


class PythonProject(Project):
    install_args = ['pip', 'install', '-r', 'requirements.txt']
    run_args = ['make', 'run']

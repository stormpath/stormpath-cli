from project import Project


class RubyProject(Project):
    install_args = ['bundle', 'install']
    run_args = ['foreman', 'start']

import sys
from os import X_OK, access, chmod, environ, makedirs, rename, unlink, pathsep
from os.path import dirname, isfile, exists, join, splitdrive, split


def get_root_path():
    """Helper function for getting the root path."""
    drive = splitdrive(sys.executable)[0]
    if drive:
        return '%s\\' % drive
    return '/'


def get_config_path(name):
    """Helper function for getting the cli config file path."""
    sp_root_dir = join(environ.get('HOME', get_root_path()), '.stormpath')
    return join(sp_root_dir, name)


def store_config_file(name, data):
    """Stores cli config file."""
    fpath = get_config_path(name)

    if not exists(dirname(fpath)):
        makedirs(dirname(fpath), 0o700)

    tmp = fpath + '.tmp'
    with open(tmp, 'w') as fd:
        fd.write(data)
        chmod(tmp, 0o400)

    rename(tmp, fpath)
    return fpath


def delete_config_file(name):
    fpath = get_config_path(name)
    unlink(fpath)
    return True


def get_config_file(name, default=None):
    """Helper function for getting the config file data."""
    fpath = get_config_path(name)

    if exists(fpath):
        return open(fpath, 'r').read()
    else:
        return default


def strip_equal_sign(arguments):
    """Helper function for a workaround against docopt adding the equal
    sign to an attribute."""
    for k, v in arguments.items():
        if v and isinstance(v, str) and (k.startswith('--') or k.startswith('-')):
            arguments.update({k: v.lstrip('=')})
            v.lstrip('=')
    return arguments


def find_non_dash_arguments_and_default_action(arguments, resource, action):
    """Sets the default action to list if no action is supplied.
    Finds all param=value pairs (ie. without dashes)"""
    from .actions import DEFAULT_ACTION
    from .resources import AVAILABLE_RESOURCES

    arguments = strip_equal_sign(arguments)
    if resource and resource.find('=') != -1:
        # Workaround for when list command is not specified
        # and non-dash attributes are used
        arguments['<attributes>'].append(resource)
        arguments['<resource>'] = None
        resource = None

    if action in AVAILABLE_RESOURCES and not resource:
        resource = action
        action = DEFAULT_ACTION

    return arguments, resource, action


def check_primary_identifier_without_flags(arguments, resource, action):
    """See if the primary attribute (ie. name/email) is supplied without
    the -n/--name flags (ie. stormpath create application 'MyApplication')
    and collect them in the <attributes> dict formated as name=value pairs."""
    from stormpath.client import Client

    for i, attr in enumerate(arguments.get('<attributes>')):
        if attr.find("=") == -1:
            if attr.startswith(Client.BASE_URL):
                arguments['<attributes>'][i] = 'href=' + attr
            else:
                primary_attr = 'email' if resource.find('account') != -1 else 'name'
                arguments['<attributes>'][i] = primary_attr + "=" + attr
    return arguments


def properly_support_boolean_values(arguments):
    def _txt_to_bool(val):
        ret = 'true' if (val == 'true' or val == '1' or val == 'True') else 'false'
        return ret

    arguments['--is-default-account-store'] = _txt_to_bool(arguments.get('--is-default-account-store'))
    arguments['--is-default-group-store'] = _txt_to_bool(arguments.get('--is-default-group-store'))
    return arguments


def which(program):
    def is_exe(fpath):
        return isfile(fpath) and access(fpath, X_OK)

    fpath, fname = split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in environ['PATH'].split(pathsep):
            path = path.strip('"')
            exe_file = join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

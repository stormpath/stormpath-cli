from os import environ, makedirs, rename, chmod, unlink
from os.path import join, dirname, exists


def get_config_path(name):
    """Helper function for getting the cli config file path."""
    sp_root_dir = join(environ.get('HOME', '/'), '.stormpath')
    return join(sp_root_dir, 'cli', name)


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

from os import environ, makedirs, rename, chmod
from os.path import join, dirname, exists


def get_config_path(name):
    return join(environ.get('HOME', '/'), '.stormpath', 'cli', name)


def store_config_file(name, data):
    fpath = get_config_path(name)

    if not exists(dirname(fpath)):
        makedirs(dirname(fpath), 0700)

    tmp = fpath + '.tmp'
    with open(tmp, 'w') as fd:
        fd.write(data)
        chmod(tmp, 0400)
    rename(tmp, fpath)
    return fpath


def get_config_file(name, default=None):
    fpath = get_config_path(name)

    if exists(fpath):
        return open(fpath, 'r').read()
    else:
        return default


def strip_equal_sign(arguments):
    for k, v in arguments.items():
        if v and isinstance(v, str) and (k.startswith('--') or k.startswith('-')):
            arguments.update({k: v.lstrip('=')})
            v.lstrip('=')
    return arguments

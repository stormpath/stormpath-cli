from stormpath.resources.application import ApplicationList
from stormpath.resources.directory import DirectoryList

from .output import get_logger
from .resources import get_resource
from .util import get_config_path, get_config_file, store_config_file, delete_config_file


def get_context_dict(quiet=True):
    """Read the current Application/Directory context from the
    cli context file."""

    data = get_config_file('context.properties')
    if not data or '=' not in data:
        return {}

    if not quiet:
        log = get_logger()
        log.info("Using context from file %s." %
            get_config_path('context.properties'))

    flag, value = data.split('=', 1)
    return {flag.strip(): value.strip()}


def _display_context():
    """Helper function for printing the current context"""
    log = get_logger()

    ctx = get_context_dict(quiet=True)
    if not ctx:
        log.info("No current context.")
        return

    flag, value = ctx.items()[0]
    if flag == '--in-application':
        typename = 'application'
    elif flag == '--in-directory':
        typename = 'directory'
    else:
        raise ValueError("Unrecognized context.")

    log.info("Current context set to the %s '%s'." % (typename, value))
    log.info("Account / Groups actions are configured to target '%s'." %
        value)


def set_context(collection, args):
    """Set the context to the requested application/directory and
    store it to the context file"""
    from .actions import _gather_resource_attributes
    args = _gather_resource_attributes(collection, args)
    value = args.get('--name') or args.get('--href')
    if not value:
        raise ValueError("Resource name or href is required.")

    if value.find('*') != -1:
        raise ValueError("Cannot use wildcard syntax when setting context.")

    # this verifies that the provided argument actually is a name
    get_resource(collection, 'name', value)

    if isinstance(collection, ApplicationList):
        flag = '--in-application'
    elif isinstance(collection, DirectoryList):
        flag = '--in-directory'
    else:
        raise ValueError("Context can only be set to Application or "
            "Directory resources")

    f = store_config_file('context.properties', '%s = %s\n' % (flag, value))
    _display_context()
    return f


def delete_context(args):
    log = get_logger()
    try:
        ret = delete_config_file('context.properties')
    except OSError:
        log.error('No context found.')
        return False
    log.info('Context cleared.')
    return ret


def show_context(args):
    _display_context()

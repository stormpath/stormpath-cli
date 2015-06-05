from __future__ import print_function
import json

from stormpath.resources.account import AccountList, Account
from stormpath.resources.application import ApplicationList
from stormpath.resources.account_store_mapping import AccountStoreMappingList
from stormpath.resources.directory import DirectoryList
from stormpath.resources.group import GroupList

from .auth import setup_credentials
from .context import set_context, show_context, delete_context
from .status import show_status
from .output import get_logger, prompt
from .resources import get_resource, get_resource_data


ATTRIBUTE_MAPS = {
    AccountList: dict(
        username = '--username',
        email = '--email',
        given_name = '--given-name',
        middle_name = '--middle-name',
        surname = '--surname',
        password = '--password',
        status = '--status',
        href = '--href',
    ),
    ApplicationList: dict(
        name = '--name',
        description = '--description',
        href = '--href',
    ),
    AccountStoreMappingList: dict(
        href = '--href',
        account_store = '--href',
        application = '--in-application',
        is_default_account_store = '--is-default-account-store',
        is_default_group_store = '--is-default-group-store',
    ),
    DirectoryList: dict(
        name = '--name',
        description = '--description',
        href = '--href',
    ),
    GroupList: dict(
        name = '--name',
        description = '--description',
        href = '--href',
    ),
}


REQUIRED_ATTRIBUTES = {
    AccountList: dict(
        email = '--email',
        given_name = '--given-name',
        surname = '--surname',
        password = '--password',
    ),
    ApplicationList: dict(
        name = '--name',
    ),
    DirectoryList: dict(
        name = '--name',
    ),
    GroupList: dict(
        name = '--name',
    ),
    AccountStoreMappingList: dict(
        application = '--in-application',
        account_store = '--href',
    )
}


EXTRA_MAPS = {
    ApplicationList: dict(
        create_directory = '--create-directory'
    )
}

SEARCH_ATTRIBUTE_MAPS = {}
for k, v in ATTRIBUTE_MAPS.items():
    v = v.copy()
    v.update(dict(status='--status', q='--query'))
    SEARCH_ATTRIBUTE_MAPS[k] = v

RESOURCE_PRIMARY_ATTRIBUTES = {
    AccountList: ['email', 'href'],
    ApplicationList: ['name', 'href'],
    DirectoryList: ['name', 'href'],
    GroupList: ['name', 'href'],
    AccountStoreMappingList: ['account_store', 'href'],
}


def _prompt_if_missing_parameters(coll, args, only_primary=False):
    required_coll_args = REQUIRED_ATTRIBUTES[type(coll)]
    all_coll_args = ATTRIBUTE_MAPS[type(coll)]
    if 'href' in all_coll_args:
        all_coll_args.pop('href')
    supplied_required_arguments = []
    for arg in required_coll_args.values():
        if arg in args and args[arg]:
            supplied_required_arguments.append(arg)

    if len(supplied_required_arguments) == required_coll_args.values():
        return args

    remaining_coll_args = {k:v for k,v in all_coll_args.items()
            if v in set(all_coll_args.values()) - set(supplied_required_arguments)}
    if remaining_coll_args:
        get_logger().info('Please enter the following information.  Fields with an asterisk (*) are required.')
        get_logger().info('Fields without an asterisk are optional.')
        for arg in sorted(remaining_coll_args):
            if arg == 'password':
                msg = args['--email']
            else:
                required = '*' if arg in required_coll_args.keys() else ''
                msg = '%s%s' % (arg.replace('_', ' ').capitalize(), required)
            v = prompt(arg, msg)
            args[all_coll_args[arg]] = v
        if type(coll) in EXTRA_MAPS:
            v = prompt(None, 'Create a directory for this application?[Y/n]')
            args['--create-directory'] = v != 'n'
    return args


def _specialized_query(coll, args, maps):
    """Formats the params in the right format before passing
    them to the needed sdk method."""
    json_rep = args.get('--json')
    if json_rep:
        try:
            return json.loads(json_rep)
        except ValueError as e:
            raise ValueError("Error parsing JSON: %s" % e)
    ctype = type(coll)
    pmap = maps.get(ctype, {})
    params = {}
    for name, opt in pmap.items():
        optval = args.get(opt)
        if optval:
            params[name] = optval
    return params


def _primary_attribute(coll, attrs):
    """Checks to see if the required primary attributes ie. identifiers like
    -n or --name are present. Each Resource can have 2 primary attributes name/email
    and the special attribute href"""
    attr_names = RESOURCE_PRIMARY_ATTRIBUTES[type(coll)]

    attr_values = [attrs.get(n) for n in attr_names if attrs.get(n)]
    if not any(attr_values):
        raise ValueError("Required attribute '%s' not specified." % ' or '.join(attr_names))
    return attr_names[0], attr_values[0]


def _gather_resource_attributes(coll, args):
    """Allows using --name/name attributes, ie. with and without the dash."""
    attrs = ATTRIBUTE_MAPS[type(coll)]

    for attr in args.get('<attributes>', []):
        if '=' not in attr:
            raise ValueError("Unknown resource attribute: " + attr)
        name, value = attr.split('=', 1)
        name = name.replace('-', '_')
        if name not in attrs:
            raise ValueError("Unknown resource attribute: " + name)
        args[attrs[name]] = value
    return args


def _add_resource_to_groups(resource, args):
    """Helper function for adding a resource to a group.
    Specifically this is only used for adding Accounts to Groups."""
    account_groups = args.get('--groups')
    if account_groups and hasattr(resource, 'add_group'):
        groups = [g.strip() for g in account_groups.split(',')]
        for group in groups:
            resource.add_group(group)
        return resource


def _check_account_store_mapping(coll, attrs):
    """Takes care of special create case for account store mappings"""

    if isinstance(coll, AccountStoreMappingList):
        attrs['application'] = {'href': attrs.get('application')}
        attrs['account_store'] = {'href': attrs.get('account_store')}

    return attrs


def list_resources(coll, args):
    """List action: Lists the requested Resource collection."""
    args = _gather_resource_attributes(coll, args)
    q = _specialized_query(coll, args, SEARCH_ATTRIBUTE_MAPS)
    if not isinstance(coll, AccountStoreMappingList):
        if q:
            coll = coll.query(**q)
    return [get_resource_data(r) for r in coll]


def create_resource(coll, args):
    """Create action: Creates a Resource."""
    args = _gather_resource_attributes(coll, args)
    _prompt_if_missing_parameters(coll, args)
    attrs = _specialized_query(coll, args, ATTRIBUTE_MAPS)
    attrs = _check_account_store_mapping(coll, attrs)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    extra = _specialized_query(coll, args, EXTRA_MAPS)

    resource = coll.create(attrs, **extra)
    _add_resource_to_groups(resource, args)

    get_logger().info('Resource created.')
    return get_resource_data(resource)


def update_resource(coll, args):
    """Update actions: Updates a Resource.
    Requires an identifier like --name."""
    args = _gather_resource_attributes(coll, args)
    attrs = _specialized_query(coll, args, ATTRIBUTE_MAPS)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    resource = get_resource(coll, attr_name, attr_value)

    for name, value in attrs.items():
        if name == attr_name or name == 'href':
            continue
        setattr(resource, name, value)
    resource.save()
    _add_resource_to_groups(resource, args)

    get_logger().info('Resource updated.')
    return get_resource_data(resource)


def delete_resource(coll, args):
    """Delete action: Deletes a Resource.
    Requires an identifier like --name or --email."""
    args = _gather_resource_attributes(coll, args)
    attrs = _specialized_query(coll, args, ATTRIBUTE_MAPS)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    resource = get_resource(coll, attr_name, attr_value)
    data = get_resource_data(resource)
    force = args.get('--force', False)

    try:
        input = raw_input
    except NameError:
        pass

    if not force:
        print("Are you sure you want to delete the following resource?")
        print(json.dumps(data, indent=2, sort_keys=True))
        resp = input('Delete this resource [y/N]? ')
        if resp.upper() != 'Y':
            return

    resource.delete()
    get_logger().info("Resource deleted.")
    if force:
        # If we're running in a script, it's useful to log exactly which
        # resource was deleted (update/create do the same)
        return data


AVAILABLE_ACTIONS = {
    'list': list_resources,
    'create': create_resource,
    'update': update_resource,
    'delete': delete_resource,
    'set': set_context,
    'context': show_context,
    'setup': setup_credentials,
    'unset': delete_context,
    'status': show_status,
}

LOCAL_ACTIONS = ('setup', 'context', 'unset', 'help')
DEFAULT_ACTION = 'list'
SET_ACTION = 'set'
STATUS_ACTION = 'status'


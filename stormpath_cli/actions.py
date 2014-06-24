from __future__ import print_function
import json

from stormpath.resources.account import AccountList, Account
from stormpath.resources.application import ApplicationList
from stormpath.resources.directory import DirectoryList
from stormpath.resources.group import GroupList

from .auth import setup_credentials
from .context import set_context, show_context, delete_context
from .output import get_logger, output
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
    ),
    ApplicationList: dict(
        name = '--name',
        description = '--description',
        href = '--href',
    ),
    DirectoryList: dict(
        name = '--name',
        description = '--description',
    ),
    GroupList: dict(
        name = '--name',
        description = '--description',
    ),
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
    AccountList: 'email',
    ApplicationList: 'name',
    DirectoryList: 'name',
    GroupList: 'name',
}


def _specialized_query(coll, args, maps):
    """Formats the params in the right format before passing
    them to the needed sdk method."""
    json_rep = args.get('--json')
    if json_rep:
        try:
            return json.loads(json_rep)
        except ValueError as e:
            raise ValueError("Error parsing JSON: {}".format(e))
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
    -n or --name are present."""
    attr_name = RESOURCE_PRIMARY_ATTRIBUTES[type(coll)]
    attr_value = attrs.get(attr_name)
    if not attr_value:
        raise ValueError("Required attribute '%s' not specified." % attr_name)
    return attr_name, attr_value


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


def list_resources(coll, args):
    """List action: Lists the requested Resource collection."""
    args = _gather_resource_attributes(coll, args)
    q = _specialized_query(coll, args, SEARCH_ATTRIBUTE_MAPS)
    if q:
        coll = coll.query(**q)
    output([get_resource_data(r) for r in coll],
        show_links = args.get('--show-links', False),
        output_json = args.get('--output-json'))


def create_resource(coll, args):
    """Create action: Creates a Resource."""
    args = _gather_resource_attributes(coll, args)
    attrs = _specialized_query(coll, args, ATTRIBUTE_MAPS)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    extra = _specialized_query(coll, args, EXTRA_MAPS)

    resource = coll.create(attrs, **extra)
    _add_resource_to_groups(resource, args)

    output(get_resource_data(resource), output_json=args.get('--output-json'))
    get_logger().info('Resource created.')


def update_resource(coll, args):
    """Update actions: Updates a Resource.
    Requires an identifier like --name."""
    args = _gather_resource_attributes(coll, args)
    attrs = _specialized_query(coll, args, ATTRIBUTE_MAPS)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    resource = get_resource(coll, attr_name, attr_value)

    for name, value in attrs.items():
        if name == attr_name:
            continue
        setattr(resource, name, value)
    resource.save()
    _add_resource_to_groups(resource, args)

    output(get_resource_data(resource), output_json=args.get('--output-json'))
    get_logger().info('Resource updated.')


def delete_resource(coll, args):
    """Delete action: Deletes a Resource.
    Requires an identifier like --name or --email."""
    args = _gather_resource_attributes(coll, args)
    attrs = _specialized_query(coll, args, ATTRIBUTE_MAPS)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    resource = get_resource(coll, attr_name, attr_value)
    data = get_resource_data(resource)
    force = args.get('--force', False)

    if not force:
        print("Are you sure you want to delete the following resource?")
        print(json.dumps(data, indent=2, sort_keys=True))
        resp = raw_input('Delete this resource [y/N]? ')
        if resp.upper() != 'Y':
            return
    else:
        # If we're running in a script, it's useful to log exactly which
        # resource was deleted (update/create do the same)
        output(data, output_json=args.get('--output-json'))

    resource.delete()
    get_logger().info("Resource deleted.")


AVAILABLE_ACTIONS = {
    'list': list_resources,
    'create': create_resource,
    'update': update_resource,
    'delete': delete_resource,
    'set': set_context,
    'context': show_context,
    'setup': setup_credentials,
    'unset': delete_context,
}

LOCAL_ACTIONS = ('setup', 'context', 'unset')
DEFAULT_ACTION = 'list'
SET_ACTION = 'set'

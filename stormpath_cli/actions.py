from __future__ import print_function
import json

from stormpath.resources.account import AccountList
from stormpath.resources.application import ApplicationList
from stormpath.resources.directory import DirectoryList
from stormpath.resources.group import GroupList

from .auth import setup_credentials
from .context import set_context, show_context
from .output import get_logger, output
from .resources import get_resource, get_resource_data


ATTRIBUTE_MAPS = {
    AccountList: dict(
        email='--email',
        full_name='--full-name',
        given_name='--given-name',
        surname='--surname',
    ),
    ApplicationList: dict(
        name='--name',
        description='--description',
    ),
    DirectoryList: dict(
        name='--name',
        description='--description',
    ),
    GroupList: dict(
        name='--name',
        description='--description',
    ),
}

EXTRA_MAPS = {
    ApplicationList: dict(
        create_directory='--create-directory'
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

def _specialized_query(args, coll, maps):
    ctype = type(coll)
    pmap = maps.get(ctype, {})

    params = {}
    for name, opt in pmap.items():
        optval = args.get(opt)
        if optval:
            params[name] = optval
    return params


def _primary_attribute(coll, attrs):
    attr_name = RESOURCE_PRIMARY_ATTRIBUTES[type(coll)]
    attr_value = attrs.get(attr_name)
    if not attr_value:
        raise ValueError("Required attribute '%s' not specified." % attr_name)
    return attr_name, attr_value


def list_resources(coll, args):
    q = _specialized_query(args, coll, SEARCH_ATTRIBUTE_MAPS)
    if q:
        coll = coll.query(**q)
    output([get_resource_data(r) for r in coll.items])


def create_resource(coll, args):
    attrs = _specialized_query(args, coll, ATTRIBUTE_MAPS)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    extra = _specialized_query(args, coll, EXTRA_MAPS)

    if extra:
        resource = coll.create(attrs, **extra)
    else:
        resource = coll.create(attrs)

    output(get_resource_data(resource))
    get_logger().info('Resource created.')


def update_resource(coll, args):
    attrs = _specialized_query(args, coll, ATTRIBUTE_MAPS)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    resource = get_resource(coll, attr_name, attr_value)

    for name, value in attrs.items():
        if name == attr_name:
            continue
        setattr(resource, name, value)
    resource.save()
    output(get_resource_data(resource))
    get_logger().info('Resource created.')


def delete_resource(coll, args):
    attrs = _specialized_query(args, coll, ATTRIBUTE_MAPS)
    attr_name, attr_value = _primary_attribute(coll, attrs)
    resource = get_resource(coll, attr_name, attr_value)
    data = get_resource_data(resource)
    force = args.get('--force', False)

    if not force:
        print("Are you sure you want to delete the following resource?")
        print(json.dumps(data, indent=2, sort_keys=True))
        resp = raw_input('Delete this resource [y/N]? ')
        if resp.upper() != 'Y':
            print("Bailig out.")
            return
    else:
        # If we're running in a script, it's useful to log exactly which
        # resource was deleted (update/create do the same)
        output(data)

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
}

LOCAL_ACTIONS = ('setup', 'context')
DEFAULT_ACTION = 'list'

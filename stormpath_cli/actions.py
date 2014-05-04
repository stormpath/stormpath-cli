from __future__ import print_function
import json

from stormpath.resources.account import AccountList
from stormpath.resources.application import ApplicationList
from stormpath.resources.directory import DirectoryList
from stormpath.resources.group import GroupList

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

SEARCH_ATTRIBUTE_MAPS = {}
for k, v in ATTRIBUTE_MAPS.items():
    v = v.copy()
    v.update(dict(status='--status', q='--query'))
    SEARCH_ATTRIBUTE_MAPS[k] = v

CREATE_ATTRIBUTE_MAPS = {}
for k, v in ATTRIBUTE_MAPS.items():
    CREATE_ATTRIBUTE_MAPS[k] = v

RESOURCE_PRIMARY_ATTRIBUTES = {
    AccountList: 'email',
    ApplicationList: 'name',
    DirectoryList: 'name',
    GroupList: 'name',
}

def _specialized_query(args, ctype, maps):
    pmap = maps.get(ctype, {})

    params = {}
    for name, opt in pmap.items():
        optval = args.get(opt)
        if optval:
            params[name] = optval
    return params


def list_resources(collection, args):
    q = _specialized_query(args, type(collection), SEARCH_ATTRIBUTE_MAPS)
    if q:
        collection = collection.query(**q)
    output([get_resource_data(r) for r in collection.items])


def create_resource(collection, args):
    properties = _specialized_query(args, type(collection),
        CREATE_ATTRIBUTE_MAPS)
    id_name = RESOURCE_PRIMARY_ATTRIBUTES[(type(collection))]
    id_value = properties.get(id_name)
    if not id_value:
        raise ValueError("Required attribute '%s' not specified." % id_name)
    resource = collection.create(properties)
    output(get_resource_data(resource))
    get_logger().info('Resource created.')


def update_resource(collection, args):
    properties = _specialized_query(args, type(collection),
        CREATE_ATTRIBUTE_MAPS)
    id_name = RESOURCE_PRIMARY_ATTRIBUTES[(type(collection))]
    id_value = properties.get(id_name)
    if not id_value:
        raise ValueError("Required attribute '%s' not specified." % id_name)

    resource = get_resource(collection, id_name, id_value)
    for name, value in properties.items():
        if name == id_name:
            continue
        setattr(resource, name, value)
    resource.save()
    output(get_resource_data(resource))
    get_logger().info('Resource created.')


def delete_resource(collection, args):
    properties = _specialized_query(args, type(collection),
        CREATE_ATTRIBUTE_MAPS)
    id_name = RESOURCE_PRIMARY_ATTRIBUTES[(type(collection))]
    id_value = properties.get(id_name)
    force = args.get('--force', False)
    if not id_value:
        raise ValueError("Required attribute '%s' not specified." % id_name)

    resource = get_resource(collection, id_name, id_value)
    data = get_resource_data(resource)

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
}

DEFAULT_ACTION = 'list'

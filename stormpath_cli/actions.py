import json

from .resources import AVAILABLE_RESOURCES

def dispatch(action):
    return AVAILABLE_ACTIONS[action]

def list_resource(client, resource, *args, **kwargs):
    sp_resource = AVAILABLE_RESOURCES[resource]
    sp_resource(client)
    data = {}
    for application in sp_resource(client):
        data[application.name] = {
            'description': application.description,
            'status': application.get_status(),
    }

    return json.dumps(data, indent=2, sort_keys=True)

def create_resource(client, resource, *args, **kwargs):
    raise NotImplementedError()

def update_resource(client, resource, *args, **kwargs):
    raise NotImplementedError()

def delete_resource(client, resource, *args, **kwargs):
    raise NotImplementedError()

def set_context(client, resource, *args, **kwargs):
    raise NotImplementedError()

AVAILABLE_ACTIONS = {
    'list': list_resource,
    'create': create_resource,
    'update': update_resource,
    'delete': delete_resource,
    'set': set_context
}

DEFAULT_ACTION = 'list'

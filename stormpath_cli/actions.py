def list_resources(resource):
    return [r._store.get_resource(r.href) for r in resource.items]

def create_resource(client, resource, *args, **kwargs):
    raise NotImplementedError()

def update_resource(client, resource, *args, **kwargs):
    raise NotImplementedError()

def delete_resource(client, resource, *args, **kwargs):
    raise NotImplementedError()

def set_context(client, resource, *args, **kwargs):
    raise NotImplementedError()

AVAILABLE_ACTIONS = {
    'list': list_resources,
    'create': create_resource,
    'update': update_resource,
    'delete': delete_resource,
    'set': set_context
}

DEFAULT_ACTION = 'list'

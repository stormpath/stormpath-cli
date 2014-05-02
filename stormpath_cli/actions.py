from stormpath.resources.account import AccountList
from stormpath.resources.application import ApplicationList
from stormpath.resources.directory import DirectoryList
from stormpath.resources.group import GroupList

SEARCH_ATTRIBUTE_MAPS = {
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
for v in SEARCH_ATTRIBUTE_MAPS.values():
    v.update(dict(status='--status', q='--query'))


def _specialized_query(args, ctype):
    qmap = SEARCH_ATTRIBUTE_MAPS.get(ctype, {})

    q = {}
    for qname, opt in qmap.items():
        optval = args.get(opt)
        if optval:
            q[qname] = optval
    return q


def list_resources(collection, args):
    q = _specialized_query(args, type(collection))
    if q:
        collection = collection.query(**q)
    return [r._store.get_resource(r.href) for r in collection.items]


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

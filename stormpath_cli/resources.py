from stormpath.client import Client


def get_resource(coll, id_name, id_value):
    if id_value.startswith(Client.BASE_URL):
        return coll.get(id_value)

    coll = coll.query(**{id_name: id_value})
    if len(coll):
        return coll[0]
    else:
        raise ValueError("The requested resource does not exist.")


def get_resource_data(resource):
    # FIXME: uses undocumented and unsupported API; this should move into the
    # SDK proper before releasing
    return resource._store.get_resource(resource.href)


def _get_context(client, args):
    a = args.get('--in-application')
    d = args.get('--in-directory')

    if a and d:
        # setting a directory overrides setting an application
        return get_resource(client.directories, 'name', d)
    elif a:
        return get_resource(client.applications, 'name', a)
    elif d:
        return get_resource(client.directories, 'name', d)
    else:
        raise ValueError("Set the context with --in-application, "
            "--in-directory or 'set'")


def get_accounts(client, args):
    return _get_context(client, args).accounts


def get_groups(client, args):
    return _get_context(client, args).groups


AVAILABLE_RESOURCES = {
    'application': lambda c, args: c.applications,
    'applications': lambda c, args: c.applications,
    'directory': lambda c, args: c.directories,
    'directories': lambda c, args: c.directories,
    'account': get_accounts,
    'accounts': get_accounts,
    'group': get_groups,
    'groups': get_groups,
}

def _get_context(client, args):
    a = args.get('--in-application')
    d = args.get('--in-directory')

    def _get_resource(coll, identifier):
        if identifier.startswith(client.BASE_URL):
            return coll.get(identifier)
        else:
            coll = coll.query(name=identifier)
            if len(coll):
                return coll[0]
            else:
                raise ValueError("The requested resource does not exist.")

    if a and d:
        raise ValueError("Can't specify both --in-application and --in-directory")
    elif a:
        return _get_resource(client.applications, a)
    elif d:
        return _get_resource(client.directories, d)
    else:
        raise ValueError("Set the context with either --in-application or --in-directory")


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

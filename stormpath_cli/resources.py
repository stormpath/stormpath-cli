def application(client, *args, **kwargs):
    return client.applications

def directory(client, *args, **kwargs):
    raise NotImplementedError()

def group(client, *args, **kwargs):
    raise NotImplementedError()

def account(client, *args, **kwargs):
    raise NotImplementedError()

def user(client, *args, **kwargs):
    raise NotImplementedError()

AVAILABLE_RESOURCES = {
    'application': application,
    'directory': directory,
    'group': group,
    'account': account,
    'user': user
}

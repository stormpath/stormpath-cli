AVAILABLE_RESOURCES = {
    'application': lambda c: c.applications,
    'applications': lambda c: c.applications,
    'directory': lambda c: c.directories,
    'directories': lambda c: c.directories,
    'account': lambda c: c.accounts,
    'accounts': lambda c: c.accounts,
    'group': lambda c: c.groups,
    'groups': lambda c: c.groups,
}

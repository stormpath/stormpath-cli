#!/usr/bin/env python

"""Usage: stormpath [<action>] [<resource>] [options]

A command-line client for the Stormpath REST API (https://stormpath.com).

Actions:
    list     List/search resources on Stormpath
    create   Create a resource on Stormpath
    update   Update a resource on Stormpath
    delete   Remove a resource from Stormpath
    set      Set context for user/group actions
    context  Show currently used context for user/group actions
    setup    Set up credentials for accessing the Stormpath API

Resources:
    application  Application Resource
    directory    Directory Resource
    group        Group Resource
    account      Account Resource
    user         User Resource

Options:
    -h, --help                              Lists help
    -v, --verbose                           Show debugging info

    -a <key:secret>, --apikey <key:secret>  Authenticate with provided key and secret
    -k <file>, --apikeyfile <file>          Use credentials from <file>
    -L, --show-links                        Show links to related resources
    -H, --show-headers                      If in TSV mode, show column headers in the first line
    -R, --create-directory                  When creating an application create the directory

List/search/create options:
    -n <name>, --name <name>                Match applications/directories/groups with name <name>
    -d <desc>, --description <desc>         Match applications/directories/groups with description <desc>
    -q <query>, --query <query>             Match resources according to the filter <query>
    -S <status>, --status <status>          Match resources with status <status>
    -s <name>, --surname <name>             Match accounts with surname <name>
    -f <name>, --full-name <name>           Match accounts with full name <name>
    -g <name>, --given-name <name>          Match accounts with given name <name>
    -e <email>, --email <email>             Match accounts with email <email>
    -u <username>, --username <username>    Account username
    -p <password>, --password <password>    Account password


Specific search options are only available for resources that have matching
attributes. Option '--query' matches on substrings, but all of the other search
options require an exact match.

Deletion flags:
    -F, --force                             Don't ask confirmation before deleting the resource

Specifying the application or directory context (for accounts and groups):
    -A <app>, --in-application <app>        Set context to application <app>
    -D <dir>, --in-directory <dir>          Set context to directory <dir>

Use json input:
    -j <json>, --json <json>                              Overrides the flags and uses json for input

For -A and -D options, the application and directory can be specified by their
name or URL.
"""

from docopt import docopt
from stormpath.client import Client
from stormpath.error import Error as StormpathError

from stormpath_cli.actions import AVAILABLE_ACTIONS, LOCAL_ACTIONS, \
    DEFAULT_ACTION
from stormpath_cli.auth import init_auth
from stormpath_cli.context import get_context_dict
from stormpath_cli.resources import AVAILABLE_RESOURCES
from stormpath_cli.output import output, setup_output

def main():
    arguments = docopt(__doc__)
    action = arguments.get('<action>')
    resource = arguments.get('<resource>')

    log = setup_output(arguments.get('--verbose'))

    arguments.update(get_context_dict())

    if action in AVAILABLE_RESOURCES and not resource:
      resource = action
      action = DEFAULT_ACTION

    if not action:
        log.error(__doc__.strip('\n'))
        return -1

    if action not in AVAILABLE_ACTIONS:
        log.error("Unknown action '%s'. See 'stormpath --help' for list of " \
            "available actions." % action)
        return -1

    if action in LOCAL_ACTIONS:
        return 0 if AVAILABLE_ACTIONS[action](arguments) else -1

    if not resource:
        log.error("A resource type is required. See 'stormpath --help' for " \
            "list of available resource types.")
        return -1

    if resource not in AVAILABLE_RESOURCES:
        log.error("Unknown resource type '%s'. See 'stormpath --help' for " \
            "list of available resource types." % resource)
        return -1

    try:
        auth_args = init_auth(arguments)
        client = Client(**auth_args)
    except ValueError as ex:
        log.error(str(ex))
        return -1

    try:
        res = AVAILABLE_RESOURCES[resource](client, arguments)
    except ValueError as ex:
        log.error(str(ex))
        return -1

    act = AVAILABLE_ACTIONS[action]

    try:
        result = act(res, arguments)
    except (StormpathError, ValueError) as ex:
        log.error(str(ex))
        return -1

    if result is not None:
        output(result,
            show_links=arguments.get('--show-links', False),
            show_headers=arguments.get('--show-headers', False))
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

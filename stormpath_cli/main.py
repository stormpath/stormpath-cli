#!/usr/bin/env python

"""Usage: stormpath [<action>] [<resource>] [options]

A command-line client for the Stormpath REST API (https://stormpath.com).

Actions:
    list    List resources on Stormpath
    create  Create a resource on Stormpath
    update  Update a resource on Stormpath
    delete  Remove a resource from Stormpath
    set     Set context for user/group actions

Resources:
    application    Application Resource
    directory      Directory Resource
    group          Group Resource
    account        Account Resource
    user           User Resource

Options:
    -h --help                               Lists help

    -a <key:secret>, --apikey <key:secret>  Authenticate with provided key and secret
    -k <file>, --apikeyfile <file>          Use credentials from <file>
    -L, --show-links                        Show links to related resources
    -H, --show-headers                      If in TSV mode, show column headers in the first line

Specifying the application or directory context (for accounts and groups):
    -A <app>, --in-application <app>        Set context to application <app>
    -D <dir>, --in-directory <dir>          Set context to directory <dir>

For -A and -D options, the application and directory can be specified by their
name or URL.
"""

from docopt import docopt
from stormpath.client import Client

from stormpath_cli.actions import AVAILABLE_ACTIONS, DEFAULT_ACTION
from stormpath_cli.auth import setup_api_key
from stormpath_cli.resources import AVAILABLE_RESOURCES
from stormpath_cli.output import output, setup_output


def main():
    log = setup_output()

    arguments = docopt(__doc__)
    action = arguments.get('<action>')
    resource = arguments.get('<resource>')

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

    if not resource:
        log.error("A resource type is required. See 'stormpath --help' for " \
            "list of available resource types.")
        return -1

    if resource not in AVAILABLE_RESOURCES:
        log.error("Unknown resource type '%s'. See 'stormpath --help' for " \
            "list of available resource types." % resource)
        return -1

    try:
        auth_args = setup_api_key(arguments)
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

    result = act(res)
    if result:
        output(result,
            show_links=arguments.get('--show-links', False),
            show_headers=arguments.get('--show-headers', False))
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

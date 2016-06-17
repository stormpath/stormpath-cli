#!/usr/bin/env python

"""Usage: stormpath [<action>] [<resource>] [options] [<attributes>...]

A command-line client for the Stormpath REST API (https://stormpath.com).

Actions:
    register Create a new Stormpath account.
    list     List/search resources on Stormpath
    create   Create a resource on Stormpath
    update   Update a resource on Stormpath
    delete   Remove a resource from Stormpath
    set      Set context for user/group actions
    context  Show currently used context for user/group actions
    setup    Set up credentials for accessing the Stormpath API
    unset    Deletes the current context
    status   Prints out authentication info and context
    deploy   Deploy your Stormpath Application to Heroku.
    run      Run a Stormpath Application.
    init     Initialize a new Stormpath sample Application.

Resources:
    application  Application Resource
    directory    Directory Resource
    group        Group Resource
    account      Account Resource
    mapping      Account Store Mapping

Options:
    -h, --help                              Lists help
    -v, --verbose                           Show debugging info

    -a <key:secret>, --apikey <key:secret>  Authenticate with provided key and secret
    -k <file>, --apikeyfile <file>          Use credentials from <file>
    -L, --show-links                        Show links to related resources
    -H, --show-headers                      If in TSV mode, show column headers in the first line
    --is-default-account-store <bool>       Used for adding mappings to current application.
    --is-default-group-store <bool>         Used for adding mappings to current application.

List/search/create options:
    -n <name>, --name <name>                Resource name. Valid for applications, directories, groups.
    -d <desc>, --description <desc>         Resource description. Valid for applications, directories and groups.
    -q <query>, --query <query>             Custom query resource collection. Valid for all resources.
    -S <status>, --status <status>          Resource status. Enum: ENABLED, DISABLED, UNVERIFIED. Valid for accounts.
    -s <name>, --surname <name>             Surname. Valid for accounts.
    -g <name>, --given-name <name>          Given name. Valid for accounts.
    -m <name>, --middle-name <name>         Middle name. Valid for accounts.
    -e <email>, --email <email>             Email address. Valid for accounts.
    -u <username>, --username <username>    Username. Valid for accounts.
    -p <password>, --password <password>    Password. Valid for accounts.
    -G <group>..., --groups <group>...      Groups to which to add a resource. Valid for accounts.
    -R, --create-directory                  When creating an application create the directory. Valid for applications.
    --href <href>                           When referencing already created Resources (ie. for update)

Init options:
    <sample-type> [<sample-name>]           When initializing a new Stormpath project, supply the type and name.
                                            Type can be: express, spring-boot, spring-boot-webmvc, ruby,
                                            laravel, flask, django, or passport.

Specific search options are only available for resources that have matching
attributes. Option '--query' matches on substrings, but all of the other search
options require an exact match.

Deletion flags:
    -F, --force                             Don't ask confirmation before deleting the resource. Valid for all resources.

Specifying the application or directory context (for accounts and groups):
    -A <app>, --in-application <app>        Set context to application <app>
    -D <dir>, --in-directory <dir>          Set context to directory <dir>

Use json input:
    -j <json>, --json <json>                Overrides the flags and uses json for input. Valid for all resources.
    --output-json                           Overrides the default human readable output to json. Valid for all resources

For -A and -D options, the application and directory can be specified by their
name or URL.
"""

import types
from sys import version_info as vi

from docopt import docopt
from stormpath.client import Client
from stormpath.error import Error as StormpathError

from stormpath_cli.actions import AVAILABLE_ACTIONS, LOCAL_ACTIONS, \
    DEFAULT_ACTION
from stormpath_cli.auth import init_auth
from stormpath_cli.context import get_context_dict
from stormpath_cli.resources import AVAILABLE_RESOURCES
from stormpath_cli.output import output, setup_output
from stormpath_cli.util import (find_non_dash_arguments_and_default_action,
    check_primary_identifier_without_flags, properly_support_boolean_values)
from stormpath_cli.actions import SET_ACTION, STATUS_ACTION

from . import __version__ as version


USER_AGENT = 'stormpath-cli/%s (python %s)' % (
    version,
    '%s.%s.%s' % (vi.major, vi.minor, vi.micro),
)


def main():
    arguments = docopt(__doc__)
    action = arguments.get('<action>')
    resource = arguments.get('<resource>')

    log = setup_output(arguments.get('--verbose'))

    arguments.update(get_context_dict())

    arguments, resource, action = find_non_dash_arguments_and_default_action(arguments, resource, action)

    arguments = properly_support_boolean_values(arguments)

    arguments = check_primary_identifier_without_flags(arguments, resource, action)

    if not action:
        log.error(__doc__.strip('\n'))
        return -1

    if action == 'help':
        log.error(__doc__.strip('\n'))
        return -1

    if action not in AVAILABLE_ACTIONS:
        log.error("Unknown action '%s'. See 'stormpath --help' for list of "
            "available actions." % action)
        return -1

    if action in LOCAL_ACTIONS:
        return 0 if AVAILABLE_ACTIONS[action](arguments) else -1

    if not resource and action != STATUS_ACTION:
        if action == SET_ACTION:
            log.error("A resource type is required. Available resources for the set command are: "
                    "application, directory. Please see 'stormpath --help'")
            return -1
        log.error("A resource type is required. Available resources: %s. "
            "Please see 'stormpath --help'" % ", ".join(sorted(AVAILABLE_RESOURCES.keys())))
        return -1

    if resource not in AVAILABLE_RESOURCES and action != STATUS_ACTION:
        log.error("Unknown resource type '%s'. See 'stormpath --help' for "
            "list of available resource types." % resource)
        return -1

    try:
        auth_args = init_auth(arguments)
        client = Client(user_agent=USER_AGENT, **auth_args)
    except ValueError as ex:
        log.error(str(ex))
        return -1

    if action == STATUS_ACTION:
        return 0 if AVAILABLE_ACTIONS[action](client, arguments) else -1

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

    if result is not None and (
            isinstance(result, list) or
            isinstance(result, dict) or
            isinstance(result, types.GeneratorType)):
        output(
            result, show_links=arguments.get('--show-links', False),
            show_headers=arguments.get('--show-headers', False),
            output_json=arguments.get('--output-json', False))
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

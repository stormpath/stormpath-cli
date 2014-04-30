#!/usr/bin/env python

"""Usage:
    stormpath [<action>] [<resource>] [options]

    Use Stormpath CLI to communicate with the Stormpath REST API.

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
      -h --help     Lists help

"""
import sys
import json
from os.path import expanduser, join
from docopt import docopt, DocoptExit
from stormpath.client import Client
from inspect import getdoc
from stormpath_cli import actions, resources

import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
# Disable requests logging
logging.getLogger("requests").propagate = False


def main():
    arguments = docopt(__doc__)
    action = arguments.get('<action>')
    resource = arguments.get('<resource>')

    if action and action not in actions.AVAILABLE_ACTIONS.keys():
        raise DocoptExit('Invalid Action. Please specify a valid action!')

    if resource not in resources.AVAILABLE_RESOURCES.keys():
        raise DocoptExit('Invalid object. Please specify a valid resource!')

    api_key_file = join(expanduser("~"), '.stormpath', 'apiKey.properties')
    client = Client(api_key_file_location=api_key_file)

    command = actions.dispatch(action)
    ret = command(client, resource)
    # this will need to log json or tab-delimited text if piped
    log.info(ret)

if __name__ == '__main__':
    main()

import unittest

try:
    from mock import create_autospec, MagicMock
except ImportError:
    from unittest.mock import create_autospec, MagicMock

from stormpath_cli import resources, actions
from stormpath_cli import output
from stormpath.client import Client
from stormpath.data_store import DataStore
from stormpath.resources.account import AccountList
from stormpath.resources.application import ApplicationList
from stormpath.resources.directory import DirectoryList
from stormpath.resources.group import GroupList

class TestActions(unittest.TestCase):

    def test_application_list_action(self):
        ds = create_autospec(DataStore)
        ds.get_resource.return_value = {
            'href': 'test/resource',
            'offset': 2,
            'limit': 25,
            'items': [
                {'href': 'test/resource'},
            ]
        }
        resource = ApplicationList(client=MagicMock(data_store=ds), properties={
            'href': '/',
            'offset': 0,
            'limit': 25,
            'items': [
                {'href': 'test/resource'},
            ]
        })

        arguments = {'<resource>': 'application', '<action>': 'list'}
        actions.list_resources(resource, arguments)
        ds.get_resource.assert_called_with('test/resource')

    def test_account_list_action(self):
        ds = create_autospec(DataStore)
        ds.get_resource.return_value = {
            'href': 'test/resource',
            'offset': 2,
            'limit': 25,
            'items': [
                {'href': 'test/resource'},
            ]
        }
        resource = AccountList(client=MagicMock(data_store=ds), properties={
            'href': '/',
            'offset': 0,
            'limit': 25,
            'items': [
                {'href': 'test/resource'},
            ]
        })

        arguments = {'<resource>': 'account', '<action>': 'list'}
        actions.list_resources(resource, arguments)
        ds.get_resource.assert_called_with('test/resource')

    def test_group_list_action(self):
        ds = create_autospec(DataStore)
        ds.get_resource.return_value = {
            'href': 'test/resource',
            'offset': 2,
            'limit': 25,
            'items': [
                {'href': 'test/resource'},
            ]
        }
        resource = GroupList(client=MagicMock(data_store=ds), properties={
            'href': '/',
            'offset': 0,
            'limit': 25,
            'items': [
                {'href': 'test/resource'},
            ]
        })

        arguments = {'<resource>': 'group', '<action>': 'list'}
        actions.list_resources(resource, arguments)
        ds.get_resource.assert_called_with('test/resource')

    def test_directory_list_action(self):
        ds = create_autospec(DataStore)
        ds.get_resource.return_value = {
            'href': 'test/resource',
            'offset': 2,
            'limit': 25,
            'items': [
                {'href': 'test/resource'},
            ]
        }
        resource = DirectoryList(client=MagicMock(data_store=ds), properties={
            'href': '/',
            'offset': 0,
            'limit': 25,
            'items': [
                {'href': 'test/resource'},
            ]
        })

        arguments = {'<resource>': 'directory', '<action>': 'list'}
        actions.list_resources(resource, arguments)
        ds.get_resource.assert_called_with('test/resource')

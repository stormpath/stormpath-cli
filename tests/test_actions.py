import unittest

try:
    from mock import create_autospec, MagicMock
except ImportError:
    from unittest.mock import create_autospec, MagicMock

from stormpath_cli import actions
from stormpath.resources.account import AccountList
from stormpath.resources.application import ApplicationList


class TestActions(unittest.TestCase):

    def test_specialized_query_gets_attributes_from_options(self):
        coll = AccountList(MagicMock(), href="test/resource")
        maps = {AccountList: {'attrname': '--foo'}}
        args = {'--foo': 'FOO', '--bar': 'BAR'}

        ret = actions._specialized_query(coll, args, maps)
        self.assertEqual(ret, {'attrname': 'FOO'})

    def test_specialized_query_loads_json_if_specified(self):
        coll = AccountList(MagicMock(), href="test/resource")
        maps = {AccountList: {'attrname': '--foo'}}
        args = {'--json': """{"attrname": "FOO"}"""}

        ret = actions._specialized_query(coll, args, maps)
        self.assertEqual(ret, {'attrname': 'FOO'})

    def test_that_resource_identifiers_are_required_and_parsed_properly(self):
        coll = ApplicationList(MagicMock(), href="test/resource")
        attrs = {'name': 'Test Application'}

        ret = actions._primary_attribute(coll, attrs)
        self.assertEqual(ret, ('name', 'Test Application'))

    def test_gathering_resource_attributes(self):
        coll = ApplicationList(MagicMock(), href="test/resource")
        args = {'<attributes>': ['name=test', 'description=test']}
        ret = actions._gather_resource_attributes(coll, args)
        self.assertEqual(ret, {
            '--name': 'test',
            '--description': 'test',
            '<attributes>': ['name=test', 'description=test']})

    def test_gathering_resource_attributes_raises_error_on_bad_syntax(self):
        coll = ApplicationList(MagicMock(), href="test/resource")
        args = {'<attributes>': ['no_eq_sign', 'description=test']}
        self.assertRaises(ValueError, actions._gather_resource_attributes, coll, args)
        args = {'<attributes>': ['no_eq_sign=', 'description=']}
        self.assertRaises(ValueError, actions._gather_resource_attributes, coll, args)

    def test_only_accounts_take_the_group_flag_into_account(self):
        args = {'--groups': 'testgroup'}
        resource = MagicMock()
        ret = actions._add_resource_to_groups(resource, args)
        self.assertIsNotNone(ret)
        resource.add_group.assert_called_once_with('testgroup')

        del resource.add_group
        ret = actions._add_resource_to_groups(resource, args)
        self.assertIsNone(ret)

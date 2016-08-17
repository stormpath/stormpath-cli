import unittest

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from stormpath_cli import context
from stormpath.resources.application import ApplicationList
from stormpath.resources.directory import DirectoryList
from stormpath.resources.account import AccountList


class TestAuth(unittest.TestCase):
    def test_getting_context_file(self):
        context.get_config_file = lambda _: '--in-application = test\n'
        ret = context.get_context_dict()
        self.assertEquals(ret, {'--in-application': 'test'})

    def test_getting_context_file_handles_invalid_syntax(self):
        context.get_config_file = lambda name: '--in-application\n'
        ret = context.get_context_dict()
        self.assertEquals(ret, {})

    def test_setting_context(self):
        context.store_config_file = lambda x, y: True
        context.get_resource = lambda x, y, z: MagicMock()
        coll = ApplicationList(MagicMock(), href="test/resource")
        args = {'--name': 'test'}
        try:
            context.set_context(coll, args)
        except:
            self.fail('Exception should not have been raised.')

    def test_setting_context_doesnt_allow_wildcard(self):
        context.store_config_file = lambda x, y: True
        context.get_resource = lambda x, y, z: MagicMock()
        coll = ApplicationList(MagicMock(), href="test/resource")
        args = {'--name': 'test*'}
        self.assertRaises(ValueError, context.set_context, coll, args)

    def test_setting_context_only_works_for_application_and_directory_resources(self):
        context.store_config_file = lambda x, y: True
        context.get_resource = lambda x, y, z: MagicMock()
        app = ApplicationList(MagicMock(), href="test/resource")
        d = DirectoryList(MagicMock(), href="test/resource")
        args = {'--name': 'test'}
        try:
            context.set_context(app, args)
        except:
            self.fail('Exception should not have been raised.')
        try:
            context.set_context(d, args)
        except:
            self.fail('Exception should not have been raised.')
        acc = AccountList(MagicMock(), href='test/resource')
        self.assertRaises(ValueError, context.set_context, acc, args)

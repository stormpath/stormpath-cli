import unittest

try:
    from mock import create_autospec, MagicMock
except ImportError:
    from unittest.mock import create_autospec, MagicMock

from stormpath_cli import resources
from stormpath.client import Client


class TestResources(unittest.TestCase):

    def test_get_resource_by_name(self):
        fake_res = {'name': 'test'}
        coll = MagicMock()
        coll.query = lambda name=None: [fake_res]
        resource = resources.get_resource(coll, 'name', 'test')
        self.assertEquals(resource, fake_res)

    def test_get_resource_by_href(self):
        fake_res = {'name': 'test'}
        coll = MagicMock()
        coll.get = lambda x: fake_res
        resource = resources.get_resource(coll, 'href', Client.BASE_URL+'/test/resource')
        self.assertEquals(resource, fake_res)

    def test_that_get_resource_raises_error_if_resource_not_found(self):
        coll = MagicMock()
        self.assertRaises(ValueError, resources.get_resource, coll, 'name', 'test')

    def test_get_context_raises_error_if_app_and_dir_both_set(self):
        client = MagicMock()
        args = {'--in-application': 'test', '--in-directory': 'test'}
        self.assertRaises(ValueError, resources._get_context, client, args)

    def test_get_context_for_applications(self):
        fake_res = {'name': 'test'}
        coll = MagicMock()
        coll.query = lambda name=None: [fake_res]
        client = MagicMock()
        client.applications = coll
        args = {'--in-application': 'test'}
        ret = resources._get_context(client, args)
        self.assertEquals(ret, fake_res)

    def test_get_context_for_directories(self):
        fake_res = {'name': 'test'}
        coll = MagicMock()
        coll.query = lambda name=None: [fake_res]
        client = MagicMock()
        client.directories = coll
        args = {'--in-directory': 'test'}
        ret = resources._get_context(client, args)
        self.assertEquals(ret, fake_res)

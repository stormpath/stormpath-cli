import unittest
import tempfile
import os

from os.path import realpath

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from stormpath_cli import auth


class TestAuth(unittest.TestCase):
    def test_init_auth_handles_the_apikey_flag_properly(self):
        args = {'--apikey': 'key:secret'}
        ret = auth.init_auth(args)
        self.assertEquals(ret, {'id': 'key', 'secret': 'secret'})

    def test_init_auth_raises_valueerror_if_incorrect_format_for_apikey_flag(self):
        args = {'--apikey': 'key_without_colon_secret'}
        self.assertRaises(ValueError, auth.init_auth, args)

    def test_init_auth_handles_the_apikeyfile_flag_properly(self):
        fd, tmpfile = tempfile.mkstemp()
        tmpfile = realpath(tmpfile)
        args = {'--apikeyfile': tmpfile}
        ret = auth.init_auth(args)
        self.assertEquals(ret, {'api_key_file_location': tmpfile})
        os.unlink(tmpfile)

    def test_init_auth_handles_the_environment_variables_with_key_and_secret(self):
        args = {}
        os.environ['STORMPATH_APIKEY_ID'] = 'key'
        os.environ['STORMPATH_APIKEY_SECRET'] = 'secret'
        ret = auth.init_auth(args)
        self.assertEquals(ret, {'id': 'key', 'secret': 'secret'})
        del os.environ['STORMPATH_APIKEY_ID']
        del os.environ['STORMPATH_APIKEY_SECRET']

    def test_init_auth_handles_the_environment_variables_with_apikeyfile(self):
        fd, tmpfile = tempfile.mkstemp()
        tmpfile = realpath(tmpfile)
        os.environ['STORMPATH_APIKEY_FILE'] = tmpfile
        args = {}
        ret = auth.init_auth(args)
        self.assertEquals(ret, {'api_key_file_location': tmpfile})
        os.unlink(tmpfile)
        del os.environ['STORMPATH_APIKEY_FILE']

    def test_that_init_auth_will_find_the_users_home_dir_and_apikeyfile(self):
        fd, tmpfile = tempfile.mkstemp()
        tmpfile = realpath(tmpfile)
        auth.get_config_path = lambda _: tmpfile
        args = {}
        ret = auth.init_auth(args)
        self.assertEquals(ret, {'api_key_file_location': tmpfile})
        os.unlink(tmpfile)

    def test_that_init_auth_will_raise_a_value_error_if_not_auth_is_found(self):
        tempdir = tempfile.mkdtemp()
        save_home = os.environ['HOME']
        os.environ['HOME'] = tempdir
        args = {}
        self.assertRaises(ValueError, auth.init_auth, args)
        os.environ['HOME'] = save_home
        os.rmdir(tempdir)

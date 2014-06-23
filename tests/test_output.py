import sys
import json
try:
    from StringIO import StringIO
except:
    from io import StringIO
import unittest

try:
    from mock import create_autospec, MagicMock
except ImportError:
    from unittest.mock import create_autospec, MagicMock

from stormpath_cli import output


class TestOutput(unittest.TestCase):

    def test_remove_links_helper(self):
        data = [{'name': 'test', 'to_remove': {'test': 'test'}}]
        ret = output._remove_links(data)
        self.assertEquals(ret, [{'name': 'test'}])

    def test_format_row(self):
        data = {'href': 'test', 'testtest': 'test'}
        max_indent = len('testtest')
        ret = output._format_row(data, 'href', max_indent)
        self.assertEquals(ret, 'href:     test\n')
        ret = output._format_row(data, 'testtest', max_indent)
        self.assertEquals(ret, 'testtest: test\n')

    def test_human_readable_output(self):
        data = [{'href': 'test'}]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            output._output_to_tty_human_readable(data=data, out=out)
            ret = out.getvalue().strip()
            self.assertEquals(ret, 'href: test')
        finally:
            sys.stdout = saved_stdout

    def test_tsv_output(self):
        data = [{'href': 'test', 'description': 'test_description'}]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            output._output_tsv(data=data, out=out)
            ret = out.getvalue().strip()
            self.assertEquals(ret, 'test_description\ttest')
        finally:
            sys.stdout = saved_stdout

    def test_json_output(self):
        data = [{'href': 'test', 'description': 'test_description'}]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            output._output_to_tty_json(data=data, out=out)
            ret = out.getvalue().strip()
            j = json.loads(ret)
            self.assertEquals(data, j)
        finally:
            sys.stdout = saved_stdout

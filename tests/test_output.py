import sys
import json
try:
    from StringIO import StringIO
except:
    from io import StringIO
import unittest

try:
    from mock import MagicMock, call
except ImportError:
    from unittest.mock import MagicMock, call

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
            output._output_tsv(data=data, show_headers=False, out=out)
            ret = out.getvalue().strip()
            self.assertEquals(ret, 'test_description\ttest')
        finally:
            sys.stdout = saved_stdout

    def test_tsv_output_with_show_headers(self):
        data = [{'href': 'test', 'description': 'test_description'}]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            output._output_tsv(data=data, show_headers=True, out=out)
            ret = out.getvalue().strip()
            self.assertEquals(ret, 'description\thref\ntest_description\ttest')
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

    def test_output_with_generator(self):
        def generate_data():
            for i in range(10):
                yield {'href': 'test%s' % i}

        data = generate_data()
        output._output = MagicMock()

        output.output(data)
        self.assertEqual(output._output.call_count, 10)
        calls = []
        for i in range(10):
            calls.append(call(
                {'href': 'test%s' % i}, output_json=False,
                show_headers=False, show_links=False))
        output._output.assert_has_calls(calls)

    def test_output_with_generator_and_output_json(self):
        def generate_data():
            for i in range(10):
                yield {'href': 'test%s' % i}

        data = generate_data()
        output._output = MagicMock()

        output.output(data, output_json=True)
        self.assertEqual(output._output.call_count, 1)
        output._output.assert_called_with(
            list(generate_data()), output_json=True, show_headers=False,
            show_links=False)

    def test_json_output_when_not_a_tty(self):
        data = [{'href': 'test', 'description': 'test_description'}]
        output._output_to_tty_json = MagicMock()

        output._output(data=data, output_json=True)
        output._output_to_tty_json.assert_called_with(data)

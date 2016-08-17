import collections
import types
from copy import deepcopy
from itertools import repeat
import json
import six
import sys
from sys import stdout
import logging


def _remove_links(data):
    """Removes nested/linked resources from the data output."""
    if not isinstance(data, list):
        data = [data]

    d2 = deepcopy(data)
    for i, el in enumerate(data):
        for k, v in el.items():
            if isinstance(v, dict) or k == 'defaultAccountStoreMapping' or k == 'defaultGroupStoreMapping':
                del d2[i][k]

    return d2


def _show_links(data):
    """Extracts hrefs from nested/linked resources from the data output."""
    if not isinstance(data, list):
        data = [data]

    d2 = deepcopy(data)
    for i, el in enumerate(data):
        for k, v in el.items():
            if isinstance(v, dict):
                d2[i][k] = d2[i][k].get('href')

    return d2


def _format_row(data, key, max_indent):
    """Helper function used for printing a human readable and
    nicely aligned output"""
    d = data[key] if data[key] else 'null'
    spacing = max_indent - len(key)
    spaces = ''.join(repeat(' ', spacing))
    row_repr = '{}: {}{}\n'.format(key, spaces, d)

    return row_repr


def _sort(data):
    """Sort the keys in the data dict alphabetically but put name and href first"""
    try:
        name = data.pop('name')
        href = data.pop('href')
    except KeyError:
        d1 = collections.OrderedDict(sorted(data.items()))
        return d1

    d1 = collections.OrderedDict(sorted(data.items()))
    d2 = collections.OrderedDict([('name', name), ('href', href)])
    d2.update(d1)

    return d2


def _output_to_tty_human_readable(data, out=stdout):
    """The default output function, used for printing a nicely aligned
    human readable output"""
    for item in data:
        if not isinstance(item, collections.OrderedDict):
            ordered_data = _sort(item)
        else:
            # already ordered in a custom way
            ordered_data = item

        max_indent = max(map(len, ordered_data.keys()))
        for key in ordered_data.keys():
            msg = _format_row(ordered_data, key, max_indent)
            out.write(msg)

        out.write('\n')


def _output_to_tty_json(data, out=stdout):
    """Helper function for printing JSON output"""
    out.write(json.dumps(data, indent=2, sort_keys=True))
    out.write('\n')


def _output_tsv(data, show_headers, out=stdout):
    """Helper function for printing tab separates values to the output.
    Used by default when CLI output is piped"""
    if not isinstance(data, list):
        data = [data]

    if not len(data):
        return

    keys = sorted(data[0].keys())

    if show_headers:
        if six.PY3:
            d = '\t'.join(keys)
        else:
            d = '\t'.join(keys).encode('utf-8')

        out.write(d)
        out.write('\n')

    def force_text(val):
        # if we're including links in TSV mode, we're only interested in href
        if isinstance(val, dict) and 'href' in val:
            return val['href']
        elif val is None:
            return ''
        else:
            return str(val)

    for row in data:
        output_row = [force_text(row[key]) for key in keys]
        if six.PY3:
            d = '\t'.join(output_row)
        else:
            d = '\t'.join(output_row).encode('utf-8')

        out.write(d)
        out.write('\n')


def _output(data, show_links=False, show_headers=False, output_json=False):
    """Output function used for printing to stdout. It will invoke the correct
    helper output function (ie. human readable/json/tsv)"""
    if not show_links:
        data = _remove_links(data)
    else:
        data = _show_links(data)

    if output_json:
        _output_to_tty_json(data)
    elif stdout.isatty():
        _output_to_tty_human_readable(data)
    else:
        _output_tsv(data, show_headers=show_headers)


def output(data, show_links=False, show_headers=False, output_json=False):
    """Main output function used for printing to stdout. It will
    invoke helper output function using generator or list and output
    total number of Resources if needed."""

    # If we have generator and don't have to output JSON, we can
    # loop throught it and output one resource at a time while
    # keeping count of them, so we can output the total later
    if isinstance(data, types.GeneratorType) and not output_json:
        resources_count = 0
        for d in data:
            _output(d, show_links=show_links, show_headers=show_headers, output_json=output_json)
            resources_count += 1

    # For every other case, we are putting resources in a list (if
    # they are not already) and outputting them all at once
    else:
        if isinstance(data, types.GeneratorType):
            data = list(data)
        elif not isinstance(data, list):
            data = [data]

        _output(data, show_links=show_links, show_headers=show_headers, output_json=output_json)
        resources_count = len(data)

    if stdout.isatty() and not output_json:
        stdout.write('\nTotal number of Resources returned: {}\n'.format(resources_count))


def get_logger():
    return logging.getLogger('stormpath_cli')


def setup_output(verbose):
    """Helper function used for setting the global logging level."""
    if verbose:
        level = logging.DEBUG
    elif stdout.isatty():
        level = logging.INFO
    else:
        level = logging.ERROR

    logging.basicConfig(format='%(message)s', level=level)
    logging.getLogger('requests').propagate = False
    return get_logger()


def _prompt_password(msg):
    from getpass import getpass

    res = getpass(prompt='Enter new password for {}*: '.format(msg))
    res2 = getpass(prompt='Confirm new password for *: '.format(msg))
    if res != res2:
        print('ERROR: Given passwords do not match!')
        sys.exit(1)

    return res


def prompt(arg, msg):
    try:
        input = raw_input
    except NameError:
        pass

    if arg == 'password':
        res = _prompt_password(msg)
    else:
        res = input(msg + ': ')

    return res

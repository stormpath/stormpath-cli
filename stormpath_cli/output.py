import collections
from itertools import repeat, imap
import json
from sys import stdout
import logging


def _remove_links(data):
    if not isinstance(data, list):
        data = [data]
    for el in data:
        for k, v in el.items():
            if isinstance(v, dict):
                del el[k]


def _format_row(data, key, max_indent):
    d = data[key] if data[key] else 'null'
    spacing = max_indent - len(key)
    spaces = "".join(repeat(" ", spacing))
    row_repr = "%s: %s%s\n" % (key, spaces, d)
    return row_repr


def _output_to_tty_human_readable(data):
    for item in data:
        # sort keys alphabetically
        ordered_data = collections.OrderedDict(sorted(item.items()))
        max_indent = max(imap(len, ordered_data.keys()))
        for key in ordered_data.keys():
            msg = _format_row(ordered_data, key, max_indent)
            stdout.write(msg)
        stdout.write("\n")


def _output_to_tty_json(data):
    stdout.write(json.dumps(data, indent=2, sort_keys=True))
    stdout.write('\n')


def _output_tsv(data, show_headers):
    if not isinstance(data, list):
        data = [data]

    if not len(data):
        return

    keys = sorted(data[0].keys())

    if show_headers:
        stdout.write(u'\t'.join(keys).encode('utf-8'))
        stdout.write('\n')

    def force_text(val):
        # if we're including links in TSV mode, we're only interested in href
        if isinstance(val, dict) and 'href' in val:
            return val['href']
        elif val is None:
            return u''
        else:
            return unicode(val)

    for row in data:
        output_row = [force_text(row[key]) for key in keys]
        stdout.write(u'\t'.join(output_row).encode('utf-8'))
        stdout.write('\n')


def output(data, show_links=False, show_headers=False, output_json=False):
    if not isinstance(data, list):
        data = [data]
    if not show_links:
        _remove_links(data)

    if stdout.isatty():
        if output_json:
            _output_to_tty_json(data)
        else:
            _output_to_tty_human_readable(data)
            stdout.write("\nTotal number of Resources returned: %s\n" %
                len(data))
    else:
        _output_tsv(data, show_headers=show_headers)


def get_logger():
    return logging.getLogger('stormpath_cli')


def setup_output(verbose):
    if verbose:
        level = logging.DEBUG
    elif stdout.isatty():
        level = logging.INFO
    else:
        level = logging.ERROR

    logging.basicConfig(format='%(message)s', level=level)
    logging.getLogger("requests").propagate = False
    return get_logger()

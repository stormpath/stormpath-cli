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


def _output_to_tty(data):
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


def output(data, show_links=False, show_headers=False):
    if not show_links:
        _remove_links(data)

    if stdout.isatty():
        _output_to_tty(data)
    else:
        _output_tsv(data, show_headers=show_headers)


def get_logger():
    return logging.getLogger('stormpath_cli')


def setup_output():
    if stdout.isatty():
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(message)s', level=logging.ERROR)
    logging.getLogger("requests").propagate = False
    return get_logger()

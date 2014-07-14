from collections import OrderedDict

from .context import _display_context, get_context_dict
from .output import _output_to_tty_human_readable
from stormpath.error import Error

def show_status(client, args):
    comm_status = 'up'
    try:
        tenant = client.tenant.name
    except Error:
        tenant = None
        comm_status = 'down'

    context = get_context_dict()

    data = [OrderedDict([
            ('API Key ID', client.auth.id),
            ('API Key Secret', client.auth.secret),
            ('Tenant', tenant),
            ('Application context', context.get('--in-application')),
            ('Directory context', context.get('--in-directory')),
            ('Group context', context.get('--in-group')),
            ('Communication Status', comm_status)
        ])
    ]

    _output_to_tty_human_readable(data)
    return True # to set correct exit codes


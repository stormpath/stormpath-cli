from __future__ import print_function

from getpass import getpass
from os import environ
from os.path import exists, join, realpath

from .output import get_logger
from .util import get_config_path, store_config_file


def init_auth(args, quiet=True):
    """Check's what authentication method to use for talking to the
    Stormpath API.

    Auth methods by descending precedence:

        apikey flag - Highest precedence
        apikeyfile flag - Evaluated if no apikey flag is set
        env variables - Evaluated if no flags are set
        apiKey.properties file in HOME directory - lowest precedence, used if no
            other method are specified.
    """
    log = get_logger()

    api_key = args.get('--apikey')
    if api_key:
        if ':' not in api_key:
            raise ValueError("API Key should be specified in id:secret format")
        key_id, key_secret = api_key.split(':', 1)
        return dict(id=key_id, secret=key_secret)

    key_file = args.get('--apikeyfile')
    if key_file:
        if not exists(key_file):
            raise ValueError("Provided API key file doesn't exist: " +
                key_file)
        key_file = realpath(key_file)
        if not quiet:
            log.info("Using API Key file %s for authentication." % key_file)
        return dict(api_key_file_location=key_file)

    key_id = environ.get('STORMPATH_APIKEY_ID')
    key_secret = environ.get('STORMPATH_APIKEY_SECRET')
    if key_id and key_secret:
        if not quiet:
            log.info("Using environment variables STORMPATH_APIKEY_ID and "
                "STORMPATH_APIKEY_SECRET for authentication.")
        return dict(id=key_id, secret=key_secret)

    api_key = environ.get('STORMPATH_APIKEY')
    if api_key and ':' in api_key:
        key_id, key_secret = api_key.split(':', 1)
        if not quiet:
            log.info("Using environment variable STORMPATH_APIKEY for "
                "authentication.")
        return dict(id=key_id, secret=key_secret)

    key_file = environ.get('STORMPATH_APIKEY_FILE')
    if key_file:
        if not exists(key_file):
            raise ValueError("API key file from STORMPATH_APIKEY_FILE "
                "environment variable doesn't exist: " + key_file)
        key_file = realpath(key_file)
        if not quiet:
            log.info("Using environment variable STORMPATH_APIKEY_FILE for "
                "authentication.")
        return dict(api_key_file_location=key_file)

    if 'HOME' in environ:
        key_file = get_config_path('apiKey.properties')
        if not exists(key_file):
            key_file = join(environ['HOME'], '.stormpath', 'apiKey.properties')

        if exists(key_file):
            key_file = realpath(key_file)
            if not quiet:
                log.info("Using API Key file %s for authentication." %
                    key_file)
            return dict(api_key_file_location=key_file)

    raise ValueError("Unable to discover an existing API Key file path "
        "or API Key environment variable.")


def _ask_for_credentials():
    """Helper function used by the setup action to prompt the user
    for auth credentials."""
    print("Please input your API Key ID and API Key Secret.")
    print("(visit http://docs.stormpath.com/rest/quickstart/"
        "#get-an-api-key for more information)")

    try:
        input = raw_input
    except NameError:
        pass

    try:
        key_id = input("API Key ID: ")
        if not key_id:
            return None
        key_secret = getpass("API Key Secret: ")
        if not key_secret:
            return None
    except KeyboardInterrupt:
        return None

    return dict(id=key_id, secret=key_secret)


def setup_credentials(arguments):
    """Setup action: Guides the user through the process
    of entering this API KEY Credentials for the Stormpath API."""
    log = get_logger()

    try:
        auth_params = init_auth(arguments, quiet=False)
    except ValueError as ex:
        log.info(str(ex))
        auth_params = _ask_for_credentials()
        if not auth_params:
            print("Bailing out.")
            return False

    kf = auth_params.get('api_key_file_location')

    if kf == get_config_path('apiKey.properties'):
        print("Stormpath CLI is set up and ready to go!")
        return True

    if kf:
        api_key_data = open(kf, 'r').read()
    else:
        api_key_data = ('apiKey.id = %s\n' % auth_params['id'] +
            'apiKey.secret = %s\n' % auth_params['secret'])

    store_config_file('apiKey.properties', api_key_data)

    print("API Key written to " + get_config_path('apiKey.properties'))
    print("Stormpath CLI is set up and ready to go!")
    return True

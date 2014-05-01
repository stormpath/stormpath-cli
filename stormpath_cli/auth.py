from os import environ
from os.path import exists, join, realpath

from .output import get_logger


def setup_api_key(args):
    log = get_logger()

    api_key = args.get('--apikey')
    if api_key:
        if ':' not in api_key:
            raise ValueError("API Key should be specified in id:secret format.")
        key_id, key_secret = api_key.split(':', 1)
        return dict(id=key_id, secret=key_secret)

    key_file = args.get('--apikeyfile')
    if key_file:
        if not exists(key_file):
            raise ValueError("Provided API key file doesn't exist: " + key_file)
        key_file = realpath(key_file)
        log.info("Using API Key file %s for authentication." % key_file)
        return dict(api_key_file_location=key_file)

    key_id = environ.get('STORMPATH_APIKEY_ID')
    key_secret = environ.get('STORMPATH_APIKEY_SECRET')
    if key_id and key_secret:
        log.info("Using environment variables STORMPATH_APIKEY_ID and " \
            "STORMPATH_APIKEY_SECRET for authentication.")
        return dict(id=key_id, secret=key_secret)

    api_key = environ.get('STORMPATH_APIKEY')
    if api_key and ':' in api_key:
        key_id, key_secret = api_key.split(':', 1)
        log.info("Using environment variable STORMPATH_APIKEY for " \
            "authentication.")
        return dict(id=key_id, secret=key_secret)

    key_file = environ.get('STORMPATH_APIKEY_FILE')
    if key_file:
        if not exists(key_file):
            raise ValueError("API key file from STORMPATH_APIKEY_FILE " \
                "environment variable doesn't exist: " + key_file)
        key_file = realpath(key_file)
        log.info("Using environment variable STORMPATH_APIKEY_FILE for " \
            "authentication.")
        return dict(api_key_file_location=key_file)

    if 'HOME' in environ:
        key_file = join(environ['HOME'], '.stormpath', 'cli',
            'apiKey.properties')
        if not exists(key_file):
            key_file = join(environ['HOME'], '.stormpath', 'apiKey.properties')

        if exists(key_file):
            key_file = realpath(key_file)
            log.info("Using API Key file %s for authentication." % key_file)
            return dict(api_key_file_location=key_file)

    raise ValueError("Unable to discover an existing API Key file path " \
        "or API Key environment variable.")

import os
import hashlib
import six

from scrapinghub.client import parse_auth
from sh_scrapy.hsref import hsref


def convert_from_bytes(data):
    if data is not None:
        data_type = type(data)
        if data_type == bytes:
            return data.decode('utf8')
        if data_type in (str, int, bool):
            return data
        if data_type == dict:
            data = data.items()
        return data_type(map(convert_from_bytes, data))


def convert_to_bytes(data):
    if data is not None:
        data_type = type(data)
        if data_type == str:
            return data.encode('utf8')
        if data_type in (bytes, int, bool):
            return data
        if data_type == dict:
            data = data.items()
        return data_type(map(convert_to_bytes, data))


def hash_mod(text, divisor):
    """
    returns the module of dividing text md5 hash over given divisor
    """
    if isinstance(text, six.text_type):
        text = text.encode('utf8')
    md5 = hashlib.md5()
    md5.update(text)
    digest = md5.hexdigest()
    return int(digest, 16) % divisor


def assign_slotno(path, numslots):
    """
    Standard way to assign slot number from url path
    """
    return str(hash_mod(path, numslots))


def get_project_id():
    """
    This method tries to extract the current project id from the environment.

    It relies on the SHUB_JOBKEY environment variable to return an integer with
    the current project id if available. It returns None otherwise.

    :return: integer with project id or None.
    """
    return hsref.projectid


def get_apikey():
    """
    This method tries to extract the current API key from the environment.

    It relies on the SHUB_JOBAUTH environment variable to return a native string
    with the current project id if available. It returns None otherwise.

    Native strings are bytes in Python 2 and unicode in Python 3.

    For compatibility reasons, if the SH_APIKEY environment variable is defined,
    we'll override the method's behavior and return this variable's parsed
    content regardless of the SHUB_JOBAUTH environment variable being set.

    :return: native string with API key or None.
    """
    if 'SH_APIKEY' in os.environ:
        return parse_auth(None)[0]

    return hsref.auth

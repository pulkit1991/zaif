from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import warnings
import inspect
import time
from datetime import datetime
from decimal import Decimal

from .compat import urlparse


def check_uri_security(uri):
    """ Warns if the uri is insecure. """
    if urlparse(uri).scheme != 'https':
        warning_message = (
            """\n\nWARNING: this client is sending a request to an insecure API endpoint. Any API request you make may expose your API key and secret to third parties. Consider using the default or a secure endpoint: \n\n\'%s\'\n
            """) % uri.replace('http','https')
        warnings.warn(warning_message, UserWarning)
    return uri


def method_name():
    """
    Returns the current active function name as a string
    """
    return inspect.stack()[1][3]


def get_nonce():
    """
    Returns nonce for use in POST data
    """
    now = datetime.now()
    nonce = str(int(time.mktime(now.timetuple())))
    microseconds = '{0:06d}'.format(now.microsecond)
    return Decimal(nonce + '.' + microseconds)

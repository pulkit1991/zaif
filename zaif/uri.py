# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
import hmac
import hashlib

from .compat import imap
from .compat import quote
from .compat import urlencode
from .errors import InvalidURIError
from .utils import get_nonce

class ApiUri(object):

    def __init__(self,key,secret,base_api_uri):
        self._key = key
        self._secret = secret
        self.BASE_API_URI = base_api_uri

    def _create_api_uri(self,*dirs):
        """
        Internal helper for creating fully qualified endpoint URIs.
        """
        return self.BASE_API_URI +'/'.join(imap(quote,dirs))

    def _make_data(self,func_name,**params):
        data = {
            'nonce': get_nonce(),
            'method':func_name,
        }
        data.update(params)
        return data

    def _make_signature(self,data):
        signature = hmac.new(bytearray(self._secret.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(urlencode(data).encode('utf-8'))
        return signature

    def _make_headers(self,data):
        signature = self._make_signature(data)
        headers = {
            'key': self._key,
            'sign': signature.hexdigest()
        }
        return headers

    # request methods
    def get(self,*dirs):
        uri = self._create_api_uri(*dirs)
        return requests.get(uri)

    def post(self,func_name,*dirs,**params):
        if not dirs:
            raise InvalidURIError('No valid URI path provided.')
        data = self._make_data(func_name,**params)
        headers = self._make_headers(data)
        uri = self._create_api_uri(*dirs)
        return requests.post(uri,data=data,headers=headers)

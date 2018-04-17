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
    """
    Convenient way to create valid API URIs and pack all the necessary data for requests to the API Server.

    If you are a consumer of the API, you shouldn't be using this class directly. It exists to be used by the Client class to make it easier to separate the functionality of API methods and API requests.
    """

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
        """
        Internal helper for creating POST request data with the client's method and its parameters.
        """
        data = {
            'nonce': get_nonce(),
            'method':func_name,
        }
        data.update(params)
        return data

    def _make_signature(self,data):
        """
        Internal helper to create signature for POST request header.
        """
        signature = hmac.new(bytearray(self._secret.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(urlencode(data).encode('utf-8'))
        return signature

    def _make_headers(self,data):
        """
        Internal helper to create headers for POST request
        """
        signature = self._make_signature(data)
        headers = {
            'key': self._key,
            'sign': signature.hexdigest()
        }
        return headers

    def get(self,*dirs):
        """
        Issues GET request to appropriately created API URI.
        Returns a HTTP response.
        """
        uri = self._create_api_uri(*dirs)
        return requests.get(uri)

    def post(self,func_name,*dirs,**params):
        """
        Issues POST request to appropriately created API URI. Raises InvalidURIError if relative paths to the BASE_API_URI are not provided.
        Returns a HTTP response.
        """
        if not dirs:
            raise InvalidURIError('No valid URI path provided.')
        data = self._make_data(func_name,**params)
        headers = self._make_headers(data)
        uri = self._create_api_uri(*dirs)
        return requests.post(uri,data=data,headers=headers)

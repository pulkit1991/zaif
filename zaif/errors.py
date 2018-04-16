# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

class ZaifError(Exception):
    """
    Base error class for all exceptions raised in this library.
    Will never be raised naked; more specific subclasses of this exception will be raised when appropriate.
    """


class ParameterRequiredError(ZaifError): pass
class InvalidURIError(ZaifError): pass

# ------------------------
# Server Error Handling
# ------------------------
class APIServerError(ZaifError):
    """
    Raised for errors related to interaction with the Zaif API server.
    """
    def __init__(self,status_code,error_msg=None):
        self.status_code = status_code
        self.error_msg = error_msg or ''

    def __str__(self):
        self.error_msg = self.error_msg.capitalize()
        return '%s %s' % (self.status_code,self.error_msg)


class NotFoundError(APIServerError): pass
class InternalServerError(APIServerError): pass
class ServiceUnavailableError(APIServerError): pass
class GatewayTimeoutError(APIServerError): pass


def api_server_error(response):
    """
    Helper method for creating errors and attaching HTTPError details to them.
    """
    error_class = _status_code_to_class.get(response.status_code,APIServerError)
    return error_class(response.status_code,response.reason)

# ------------------------
# Response Error Handling
# ------------------------
class APIResponseError(ZaifError):
    """
    Raised for errors details included in 200 responses.
    """
    def __init__(self,error_msg=None):
        self.error_msg = error_msg or ''

    def __str__(self):
        self.error_msg = self.error_msg.capitalize()
        return '%s' % self.error_msg


def api_response_error(response_json):
    """
    Helper method to raise errors using error details included in the response.
    """
    error_msg = response_json.get('error',None)
    return APIResponseError(error_msg)



_status_code_to_class = {
    404: NotFoundError,
    500: InternalServerError,
    503: ServiceUnavailableError,
    504: GatewayTimeoutError,
}

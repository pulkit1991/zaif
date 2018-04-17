# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from .uri import ApiUri
from .utils import method_name
from .utils import check_uri_security
from .errors import api_server_error
from .errors import api_response_error
from .errors import ParameterRequiredError

class Client(object):
    """ API Client for the Zaif REST API.
    Entry point for making requests to the Zaif REST API.

    Provides helper methods for common API endpoints, as well as niceties around response handling.

    Any errors will be raised as exceptions. These exceptions will always be subclasses of `zaif.error.ZaifError`. HTTP-related errors will be subclasses of `zaif.errors.APIServerError` and Errors in Responses will be subclasses of `zaif.errors.APIResponseError`.

    Full API docs, including descriptions of each API and its parameters, are available here: http://techbureau-api-document.readthedocs.io/ja/latest/index.html
    """

    BASE_API_URI = 'https://api.zaif.jp/'

    def __init__(self,key,secret,base_api_uri=None):
        if not key:
            raise ValueError("Missing API 'key'")
        if not secret:
            raise ValueError("Missing API 'secret'")
        self._key = key
        self._secret = secret
        # Allow passing in a different API base and warn if it is insecure.
        self.BASE_API_URI = check_uri_security(base_api_uri or self.BASE_API_URI)
        self._api_uri = ApiUri(key,secret,self.BASE_API_URI)

    def _handle_response(self,response):
        """
        Internal helper for handling API responses from the Zaif server. Raises the appropriate server errors when response is not 200; otherwise, parses the response.
        """
        if response.status_code != 200:
            raise api_server_error(response)
        return self._parse_response(response)

    def _parse_response(self,response):
        """
        Returns the json data in case of PUBLIC API and FUTURES API reponses.
        For TRADING API and LEVERAGE API, returns the json data if the response is a success, otherwise raises APIResponseError.
        """
        response_json = response.json()
        if isinstance(response_json,dict):
            success = response_json.pop('success',None)
            if success==1:
                return response_json['return']
            elif success==0:
                raise api_response_error(response_json)
        return response_json


    def _check_req_params(self,req_params,params):
        """
        Internal helper to check if all required parameters for the method have been provided. Raises ParameterRequiredError if any of the required parameters is missing.
        """
        if not all(req_p in params for req_p in req_params):
            raise ParameterRequiredError('Missing required parameter(s) %s' % req_params)

    # --------------------
    #   PUBLIC API
    # --------------------
    def _public(self,*dirs):
        """
        Helper method to execute get request to public API URI
        """
        return self._api_uri.get('api','1',*dirs)

    def get_currencies(self):
        response = self._public('currencies','all')
        return self._handle_response(response)

    def get_currency(self,currency):
        response = self._public('currencies',currency)
        return self._handle_response(response)

    def get_currency_pairs(self):
        response = self._public('currency_pairs','all')
        return self._handle_response(response)

    def get_currency_pair(self,currency_pair):
        response = self._public('currency_pairs',currency_pair)
        return self._handle_response(response)

    def get_last_price(self,currency_pair):
        response = self._public('last_price',currency_pair)
        return self._handle_response(response)

    def get_ticker(self,currency_pair):
        response = self._public('ticker',currency_pair)
        return self._handle_response(response)

    def get_trades(self,currency_pair):
        response = self._public('trades',currency_pair)
        return self._handle_response(response)

    def get_depth(self,currency_pair):
        response = self._public('depth',currency_pair)
        return self._handle_response(response)

    # --------------------
    #   TRADING API
    # --------------------
    def _trading(self,func_name,**params):
        """
        Helper method to execute post request to trading API URI
        """
        return self._api_uri.post(func_name,'tapi',**params)

    def get_info(self):
        response = self._trading(method_name())
        return self._handle_response(response)

    def get_info2(self):
        response = self._trading(method_name())
        return self._handle_response(response)

    def get_personal_info(self):
        response = self._trading(method_name())
        return self._handle_response(response)

    def get_id_info(self):
        response = self._trading(method_name())
        return self._handle_response(response)

    def get_trade_history(self,**params):
        response = self._trading('trade_history',**params)
        return self._handle_response(response)

    def get_active_orders(self,**params):
        response = self._trading('active_orders',**params)
        return self._handle_response(response)

    def trade(self,**params):
        req_params = ['currency_pair','action','price','amount']
        self._check_req_params(req_params,params)
        response = self._trading(method_name(),**params)
        return self._handle_response(response)

    def buy(self,**params):
        return self.trade(action='bid',**params)

    def sell(self,**params):
        return self.trade(action='ask',**params)

    def cancel_order(self,**params):
        req_params = ['order_id']
        self._check_req_params(req_params,params)
        response = self._trading(method_name(),**params)
        return self._handle_response(response)

    def withdraw(self,**params):
        req_params = ['currency','address','amount']
        self._check_req_params(req_params,params)
        response = self._trading(method_name(),**params)
        return self._handle_response(response)

    def get_deposit_history(self,**params):
        req_params = ['currency']
        self._check_req_params(req_params,params)
        response = self._trading('deposit_history',**params)
        return self._handle_response(response)

    def get_withdraw_history(self,**params):
        req_params = ['currency']
        self._check_req_params(req_params,params)
        response = self._trading('withdraw_history',**params)
        return self._handle_response(response)


    # --------------------
    #   FUTURES API
    # --------------------
    def _futures(self,*dirs):
        """
        Helper method to execute get request to futures API URI
        """
        return self._api_uri.get('fapi','1',*dirs)

    def get_groups(self):
        response = self._futures('groups','all')
        return self._handle_response(response)

    def get_group(self,group_id):
        response = self._futures('groups',group_id)
        return self._handle_response(response)

    def get_group_last_price(self,group_id,currency_pair):
        response = self._futures('last_price',group_id,currency_pair)
        return self._handle_response(response)

    def get_group_ticker(self,group_id,currency_pair):
        response = self._futures('ticker',group_id,currency_pair)
        return self._handle_response(response)

    def get_group_trades(self,group_id,currency_pair):
        response = self._futures('trades',group_id,currency_pair)
        return self._handle_response(response)

    def get_group_depth(self,group_id,currency_pair):
        response = self._futures('depth',group_id,currency_pair)
        return self._handle_response(response)

    # --------------------
    #   LEVERAGE API
    # --------------------
    def _leverage(self,func_name,**params):
        """
        Helper method to execute post request to leverage API URI
        """
        return self._api_uri.post(func_name,'tlapi',**params)

    def get_positions(self,**params):
        req_params = ['type','group_id']
        self._check_req_params(req_params,params)
        response = self._leverage(method_name(),**params)
        return self._handle_response(response)

    def get_position_history(self,**params):
        req_params = ['type','group_id','leverage_id']
        self._check_req_params(req_params,params)
        response = self._leverage('position_history',**params)
        return self._handle_response(response)

    def get_active_positions(self,**params):
        req_params = ['type','group_id']
        self._check_req_params(req_params,params)
        response = self._leverage('active_positions',**params)
        return self._handle_response(response)

    def create_position(self,**params):
        req_params = ['type', 'group_id', 'currency_pair', 'action', 'price', 'amount', 'leverage']
        self._check_req_params(req_params,params)
        response = self._leverage(method_name(),**params)
        return self._handle_response(response)

    def create_buy_position(self,**params):
        return self.create_position(action='bid',**params)

    def create_sell_position(self,**params):
        return self.create_position(action='ask',**params)

    def change_position(self,**params):
        req_params = ['type','group_id','leverage_id','price']
        self._check_req_params(req_params,params)
        response = self._leverage(method_name(),**params)
        return self._handle_response(response)

    def cancel_position(self,**params):
        req_params = ['type','group_id','leverage_id']
        self._check_req_params(req_params,params)
        response = self._leverage(method_name(),**params)
        return self._handle_response(response)

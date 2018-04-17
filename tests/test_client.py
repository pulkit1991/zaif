# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
import unittest2
import json
import re
import warnings
import httpretty as hp

from zaif import errors
from zaif.client import Client

# Hide all warning output.
warnings.showwarning = lambda *a, **k: None

# Dummy API key values for use in tests
api_key = 'fakeapikey'
api_secret = 'fakeapisecret'

mock_items = {'key1': 'val1', 'key2': 'val2'}
mock_collection = [mock_items, mock_items]


class TestClient(unittest2.TestCase):
    def test_key_and_secret_required(self):
        with self.assertRaises(ValueError):
            Client(None,api_secret)
        with self.assertRaises(ValueError):
            Client(api_key,None)

    @hp.activate
    def test_base_api_uri_used_instead_of_default(self):
        # Requests to the default BASE_API_URI will noticeably fail by raising an AssertionError. Requests to the new URL will respond HTTP 200.
        new_base_api_uri = 'https://api.zaif.jp/new/'
        # If any error is raised by the server, the test suite will never exit when using Python 3. This strange technique is used to raise the errors outside of the mocked server environment.
        errors_in_server = []
        def mock_response(request,uri,headers):
            try:
                self.assertEqual(uri,new_base_api_uri)
            except AssertionError as e:
                errors_in_server.append(e)
            return 200,headers,'{}'

        hp.register_uri(hp.GET,Client.BASE_API_URI,mock_response)
        hp.register_uri(hp.GET,new_base_api_uri,mock_response)

        client = Client(api_key,api_secret) # default BASE_API_URI
        client_new = Client(api_key,api_secret,new_base_api_uri)

        self.assertEqual(client_new._api_uri.get().status_code,200)
        with self.assertRaises(AssertionError):
            client._api_uri.get()
            if errors_in_server:
                raise errors_in_server.pop()

    @hp.activate
    def test_http_base_api_uri_issues_uri_security_warning(self):
        insecure_url = 'http://api.zaif.jp/'
        with self.assertWarns(UserWarning):
            client = Client(api_key,api_secret,insecure_url)
            # check if response receieved even with insecure_url
            mock_response = {'body':'{}',
                             'status':200}
            hp.register_uri(hp.GET,insecure_url,**mock_response)
            self.assertEqual(client._api_uri.get().status_code,200)


    @hp.activate
    def test_200_response_handling(self):
        # check if 200 response returns the json data
        client = Client(api_key, api_secret)
        mock_response = {'body':json.dumps(mock_collection),
                         'status':200}
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        response = client._api_uri.get('test')
        self.assertEqual(client._handle_response(response),mock_collection)

        # check if 200 response with success==1 also returns the json data
        mock_response = {'body':json.dumps({'success':1,
                                            'return':mock_items}),
                         'status':200}
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        response = client._api_uri.get('test')
        self.assertEqual(client._handle_response(response),mock_items)

    @hp.activate
    def test_server_error_handling(self):
        client = Client(api_key, api_secret)

        for ecode,eclass in six.iteritems(errors._status_code_to_class):
            mock_response = {'body':json.dumps('{}'),
                             'status':ecode}
            hp.register_uri(hp.GET,re.compile('.*'+str(ecode)+'$'),**mock_response)
            with self.assertRaises(eclass):
                client._handle_response(client._api_uri.get(str(ecode)))

        # check if status code is unrecognized, generic APIServerError is raised
        mock_response = {'status':418}
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        with self.assertRaises(errors.APIServerError):
            client._handle_response(client._api_uri.get('test'))


    @hp.activate
    def test_response_error_handling(self):
        client = Client(api_key, api_secret)
        # check if appropriate error is raised depending on status code
        # AND if error data is in response, it is used
        error_body = {'success':0,
                      'error': 'some error message'}
        mock_response = {'body':json.dumps(error_body),
                         'status':200}
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        with self.assertRaises(errors.APIResponseError):
            client._handle_response(client._api_uri.get('test'))


    # --------------------
    #   TEST PUBLIC API
    # --------------------
    @hp.activate
    def test_public_helper_creates_correct_uri(self):
        mock_response = {'body':json.dumps('{}')}
        client = Client(api_key,api_secret)
        hp.register_uri(hp.GET,re.compile('.*api/1/foo/bar$'),**mock_response)
        self.assertEqual(client._public('foo','bar').status_code,200)
        hp.reset()

    @hp.activate
    def test_get_currencies(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*api/1/currencies/all$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_currencies(),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_currency(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*api/1/currencies/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_currency('foo'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_currency_pairs(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*api/1/currency_pairs/all$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_currency_pairs(),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_currency_pair(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*api/1/currency_pairs/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_currency_pair('foo'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_last_price(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*api/1/last_price/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_last_price('foo'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_ticker(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*api/1/ticker/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_ticker('foo'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_trades(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*api/1/trades/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_trades('foo'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_depth(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*api/1/depth/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_depth('foo'),mock_collection)
        hp.reset()

    # --------------------
    #   TEST TRADING API
    # --------------------
    @hp.activate
    def test_trading_helper_automatically_encodes_data(self):
        client = Client(api_key,api_secret)
        def mock_response(request,uri,headers):
            self.assertIsInstance(request.body, six.binary_type)
            return 200,headers,'{}'
        hp.register_uri(hp.POST,re.compile('.*tapi$'),mock_response)
        self.assertEqual(client._trading('foo').status_code,200)
        hp.reset()


    @hp.activate
    def test_get_info(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_info(),mock_items)
        hp.reset()

    @hp.activate
    def test_get_info2(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_info2(),mock_items)
        hp.reset()

    @hp.activate
    def test_get_personal_info(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_personal_info(),mock_items)
        hp.reset()

    @hp.activate
    def test_get_id_info(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_id_info(),mock_items)
        hp.reset()

    @hp.activate
    def test_get_trade_history(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_trade_history(),mock_items)
        hp.reset()

    @hp.activate
    def test_get_active_orders(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_active_orders(),mock_items)
        hp.reset()

    @hp.activate
    def test_trade(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'currency_pair':'eth_btc',
                      'action':'bid',
                      'price':100.0,
                      'amount':1.0}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.trade(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.trade(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_buy(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'currency_pair':'eth_btc',
                      'price':100.0,
                      'amount':1.0}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.buy(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.buy(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_sell(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'currency_pair':'eth_btc',
                      'price':100.0,
                      'amount':1.0}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.sell(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.sell(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_cancel_order(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'order_id':'123'}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.cancel_order(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.cancel_order(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_withdraw(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'currency':'ETH',
                      'address':'0x1234abcd5678efgh',
                      'amount':1.5}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.withdraw(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.withdraw(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_get_deposit_history(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'currency':'ETH'}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.get_deposit_history(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.get_deposit_history(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_get_withdraw_history(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'currency':'ETH'}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.get_withdraw_history(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.get_withdraw_history(**send_params),mock_items)
        hp.reset()

    # --------------------
    #   TEST FUTURES API
    # --------------------
    @hp.activate
    def test_futures_helper_creates_correct_uri(self):
        mock_response = {'body':json.dumps('{}')}
        client = Client(api_key,api_secret)
        hp.register_uri(hp.GET,re.compile('.*fapi/1/foo/bar$'),**mock_response)
        self.assertEqual(client._futures('foo','bar').status_code,200)
        hp.reset()

    @hp.activate
    def test_get_groups(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*fapi/1/groups/all$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_groups(),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_group(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*fapi/1/groups/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_group('foo'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_group_last_price(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*fapi/1/last_price/foo/bar$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_group_last_price('foo','bar'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_group_ticker(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*fapi/1/ticker/foo/bar$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_group_ticker('foo','bar'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_group_trades(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*fapi/1/trades/foo/bar$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_group_trades('foo','bar'),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_group_depth(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*fapi/1/depth/foo/bar$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_group_depth('foo','bar'),mock_collection)
        hp.reset()

    # --------------------
    #   TEST LEVERAGE API
    # --------------------
    @hp.activate
    def test_leverage_helper_automatically_encodes_data(self):
        client = Client(api_key,api_secret)
        def mock_response(request,uri,headers):
            self.assertIsInstance(request.body, six.binary_type)
            return 200,headers,'{}'
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),mock_response)
        self.assertEqual(client._leverage('foo').status_code,200)
        hp.reset()

    @hp.activate
    def test_get_positions(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'type':'futures',
                      'group_id':'1'}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.get_positions(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.get_positions(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_get_position_history(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'type':'futures',
                      'group_id':'1',
                      'leverage_id':'123'}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.get_position_history(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.get_position_history(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_get_active_positions(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'type':'futures',
                      'group_id':'1'}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.get_active_positions(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.get_active_positions(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_create_position(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'type':'margin',
                      'group_id':'1',
                      'currency_pair':'eth_btc',
                      'action':'ask',
                      'price':100,
                      'amount':0.5,
                      'leverage':3.25}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.create_position(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.create_position(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_create_buy_position(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'type':'margin',
                      'group_id':'1',
                      'currency_pair':'eth_btc',
                      'price':100,
                      'amount':0.5,
                      'leverage':3.25}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.create_buy_position(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.create_buy_position(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_create_sell_position(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'type':'margin',
                      'group_id':'1',
                      'currency_pair':'eth_btc',
                      'price':100,
                      'amount':0.5,
                      'leverage':3.25}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.create_sell_position(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.create_sell_position(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_change_position(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'type':'futures',
                      'group_id':'1',
                      'leverage_id':'123',
                      'price':100}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.change_position(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.change_position(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_cancel_position(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*tlapi$'),**mock_response)
        client = Client(api_key,api_secret)

        req_params = {'type':'futures',
                      'group_id':'1',
                      'leverage_id':'123'}
        send_params = {}
        while req_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.change_position(**send_params)
            for key in req_params:
                send_params[key] = req_params.pop(key)
                break

        self.assertEqual(client.cancel_position(**send_params),mock_items)
        hp.reset()

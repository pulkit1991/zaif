# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
import unittest2
import json
import re
import httpretty as hp

from zaif.errors import InvalidURIError
from zaif.uri import ApiUri


# Dummy API key values for use in tests
api_key = 'fakeapikey'
api_secret = 'fakeapisecret'
base_api_uri ='https://api.foo.bar/'

mock_items = {'key1': 'val1', 'key2': 'val2'}


class TestUtils(unittest2.TestCase):
    @hp.activate
    def test_get_and_post_methods_succeed_with_string_and_unicode(self):
        mock_response = {'body':json.dumps(mock_items),
                         'status':200}
        hp.register_uri(hp.GET,re.compile('.*get_test$'),**mock_response)
        hp.register_uri(hp.POST,re.compile('.*post_test$'),**mock_response)

        # String
        key = 'fakekey'
        secret = 'fakesecret'
        self.assertIsInstance(key, six.string_types)
        self.assertIsInstance(secret, six.string_types)
        api_uri = ApiUri(key,secret,base_api_uri)
        self.assertEqual(api_uri.get('get_test').status_code,200)
        self.assertEqual(api_uri.post('fakefunc','post_test').status_code,200)

        # Unicode
        key = u'fakekey'
        secret = u'fakesecret'
        self.assertIsInstance(key, six.text_type)
        self.assertIsInstance(secret, six.text_type)
        api_uri = ApiUri(key,secret,base_api_uri)
        self.assertEqual(api_uri.get('get_test').status_code,200)
        self.assertEqual(api_uri.post('fakefunc','post_test').status_code,200)

    @hp.activate
    def test_get_method_fetches_data_from_correct_uri_path(self):
        mock_response = {'body':json.dumps(mock_items),
                         'status':200}
        hp.register_uri(hp.GET,re.compile('.*baz/test$'),**mock_response)
        api_uri = ApiUri(api_key,api_secret,base_api_uri)
        self.assertEqual(api_uri.get('baz','test').status_code,200)

    @hp.activate
    def test_post_method_raises_invalid_uri_error(self):
        mock_response = {'body':json.dumps(mock_items),
                         'status':200}
        hp.register_uri(hp.POST,re.compile('.*test$'),**mock_response)
        api_uri = ApiUri(api_key,api_secret,base_api_uri)
        with self.assertRaises(InvalidURIError):
            api_uri.post(api_uri.post('fakefunc'))

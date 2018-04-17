zaif
===================

REST API Client for Zaif Exchange

|logo|

.. |logo| image:: https://bitcoin-matome.info/wp-content/uploads/2014/10/zaif-logo-300x150.png

Features
=========

- A single client to call any type of API (public, trading, futures, leveraged)
- Convenient methods for making API calls using keyword arguments - packs JSON for you!
- Near 100% test coverage.
- Tab-completable methods and attributes when using `IPython <http://ipython.org/>`_.
- Supports both Python 2 and Python 3

Installation
=============

``zaif`` is available on `PYPI <https://pypi.python.org/pypi>`_. Install with ``pip``:

.. code:: bash

    $ pip install zaif

or with ``easy_install``:

.. code:: bash

    $ easy_install zaif

The library is currently tested against Python versions 2.7 and 3.4+.

API Reference
===============

The official documentation can be found on the `Zaif API reference page <http://techbureau-api-document.readthedocs.io/ja/latest/index.html>`_.


Prerequisites
===============

The first thing you need to do is to `Sign Up with Zaif <https://zaif.jp>`_.

Next, you need to obtain an **API Key** and an **API Secret**. If you're writing code for your own Zaif account, you can create API keys on `Zaif API Settings <https://zaif.jp/api_keys>`_ page. You can create multiple API keys with different permissions for your applications.

NOTE: Make sure to enable appropriate permissions for the API key.

Getting started
=================

Create a ``Client`` object for interacting with the API:

.. code:: python

    from zaif.client import Client

    api_key = 'your api key'
    api_secret = 'your api secret'

    client = Client(api_key,api_secret)

Error handling
--------------
All errors occurring during interaction with the API will be raised as exceptions. These exceptions will be subclasses of ``zaif.errors.ZaifError``.

* When the error involves the API server, the error raised will be a subclass of ``zaif.errors.APIServerError``.
* When the error is associated with response received form the API server, ``zaif.errors.APIResponseError`` will be raised.

For full details of error responses, please refer to the `relevant API documentation <http://techbureau-api-document.readthedocs.io/ja/latest/index.html>`_.

+---------------------------+----------------------+
|            Error          |   HTTP Status code   |
+===========================+======================+
| NotFoundError             |          404         |
+---------------------------+----------------------+
| InternalServerError       |          500         |
+---------------------------+----------------------+
| ServiceUnavailableError   |          503         |
+---------------------------+----------------------+
| GatewayTimeoutError       |          504         |
+---------------------------+----------------------+

Usage
-------
I've done my best to make the code clean, commented, and understandable; however it may not be exhaustive. For more details, please refer to the `Zaif API official documentation <http://techbureau-api-document.readthedocs.io/ja/latest/index.html>`_.

**In short**

- **Use args for URI paths**
- **Use kwargs for formData or query parameters**


**PUBLIC API (Market Data)**

Get available currencies, tokens, ICO etc.

.. code:: python

    client.get_currencies()
    client.get_currency('BTC')


Get currency pairs traded on the exchange.

.. code:: python

    client.get_currency_pairs()
    client.get_currency_pair('eth_btc')

Get current closing price for a currency pair

.. code:: python

    client.get_ticker('eth_btc')


Get ticker information for a currency pair

.. code:: python

    client.get_ticker('eth_btc')


Get trades for a currency pair

.. code:: python

    client.get_trades('eth_btc')


Get board information (asks, bids) for a currency pair

.. code:: python

    client.get_depth('eth_btc')


**TRADING API**

Get current balance (asset and token balances), API key permissions, number of past trades, number of open orders, server timestamp.

.. code:: python

    client.get_info()

It is a lightweight version of ``get_info()`` and returns items excluding past trades

.. code:: python

    client.get_info2()

Get nickname and icon image path for your account

.. code:: python

    client.get_personal_info()

Get account information such as user ID, email, etc.

.. code:: python

    client.get_id_info()

Get trade history

.. code:: python

    client.get_trade_history()


Get a list of active orders (currency pairs and tokens)

.. code:: python

    client.get_active_orders(currency_pair='eth_btc')


Create a new trading order

.. code:: python

    client.trade(currency_pair='eth_btc',
                 action='bid',
                 price=100,
                 amount=1.5)


Convenient function to create a buy order

.. code:: python

    client.buy(currency_pair='eth_btc',price=100,amount=1.5)

Convenient function to create a sell order

.. code:: python

    client.sell(currency_pair='eth_btc',price=100,amount=1.5)


Cancel an open order

.. code:: python

    client.cancel_order(order_id=123)


Withdraw currency to a specific address

.. code:: python

    client.withdraw(currency='ETH',address='0x1234abcd5678efgh',amount=1)


Get deposit payments (account funding) history for a currency

.. code:: python

    client.get_deposit_history(currency='BTC')

Get history of withdrawals for a currency

.. code:: python

    client.get_withdraw_history(currency='BTC')


**FUTURES API**

Get information on futures transactions

.. code:: python

    client.get_groups()

Get information on a specific futures transaction

.. code:: python

    client.get_group(2)


Get last on a specific futures transaction

.. code:: python

    client.get_group_last_price(2)


Get ticker for a futures transaction

.. code:: python

    client.get_group_ticker(2)

Get all trades of a futures transaction

.. code:: python

    client.get_group_trades(2)

Get board information of a futures transaction

.. code:: python

    client.get_group_depth(2)


**LEVERAGE API**

Get history of your leveraged trades

.. code:: python

    client.get_positions(type='futures',group_id=1)

Get detailed history of your leveraged trades

.. code:: python

    client.get_positions(type='futures',group_id=1,leverage_id=123)

Get currently valid order list of leveraged transactions

.. code:: python

    client.get_active_positions(type='futures',group_id=1)

Create a new leveraged transaction

.. code:: python

    client.create_position(type='futures',
                           group_id=1,
                           currency_pair='eth_btc',
                           action='ask',
                           price=100.0,
                           amount=1,
                           leverage=3.25)



Convenient method to create a new leveraged buy transaction

.. code:: python

    client.create_buy_position(type='futures',
                               group_id=1,
                               currency_pair='eth_btc',
                               price=100.0,
                               amount=1,
                               leverage=3.25)


Convenient method to create a new leveraged sell transaction

.. code:: python

    client.create_sell_position(type='futures',
                                group_id=1,
                                currency_pair='eth_btc',
                                price=100.0,
                                amount=1,
                                leverage=3.25)


Modify a leveraged transaction

.. code:: python

    client.change_position(type='margin',group_id=1,leverage_id=123)

Cancel a leveraged transaction

.. code:: python

    client.cancel_position(type='margin',group_id=1,leverage_id=123)



Testing / Contributing
=======================
Any contribution is welcome! The process is simple:

* Fork this repo
* Make your changes
* Run the tests (for multiple versions: preferred)
* Submit a pull request.


Testing for your current python version
------------------------------------------

Tests are run via `nosetest <https://nose.readthedocs.io/en/latest/>`_. To run the tests, clone the repository and then:

.. code:: bash

    # Install the required dependencies
    $ pip install -r requirements.txt
    $ pip install -r test-requirements.txt

    # Run the tests
    $ make tests


If you'd also like to generate an HTML coverage report (useful for figuring out which lines of code are actually being tested), make sure the requirements are installed and then run:

.. code:: bash

    $ make coverage


Testing for multiple python versions
------------------------------------------

I am using `tox <http://tox.readthedocs.io/en/latest/install.html>`_ to run the test suite against multiple versions of Python. Tox requires the appropriate Python interpreters to run the tests in different environments. I would recommend using `pyenv <https://github.com/pyenv/pyenv#installation>`_ for this.


However, the process is a little unintuitive because ``tox`` does not seem to work with multiple versions of python (installed via ``pyenv``) when inside a ``pyenv`` virtual environment. So, first deactivate your pyenv virtual environment:

.. code:: bash

    $ (zaifapi-venv) pyenv deactivate


and then install `tox` with pip or easy_install:

.. code:: bash

    $ pip install tox # or
    $ easy_install tox


Install python versions which you want to test:

.. code:: bash

    $ pyenv install 2.7.14
    $ pyenv install 3.5.0
    $ pyenv install 3.6.0

and so forth. Now, in your project directory:

.. code:: bash

    # all versions which are in tox.ini file
    $ pyenv local 2.7.14 3.5.0 3.6.0

    # run the tests for all the above versions
    $ tox


License
=========

This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
=================

- `zaifapi <https://github.com/techbureau/zaifapi>`_

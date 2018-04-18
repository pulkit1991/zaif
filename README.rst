zaif
===================

REST API Client for Zaif Exchange

Zaif Exchange用のREST APIクライアント

|logo|

.. |logo| image:: https://bitcoin-matome.info/wp-content/uploads/2014/10/zaif-logo-300x150.png

Features
=========

- A single client to call any type of API (public, trading, futures, leveraged). 任意の種類のAPI（公開、取引、先物、レバレッジド）を呼び出す単一のクライアント。
- Convenient methods for making API calls using keyword arguments - packs JSON for you! キーワード引数を使用してAPIコールを作成するための便利なメソッド - JSONをパック！
- Near 100% test coverage. 100％近いテストカバレッジ。
- Tab-completable methods and attributes when using `IPython <http://ipython.org/>`_. `IPython <http://ipython.org/>`_ を使用した場合のタブで完成可能なメソッドと属性。
- Supports both Python 2 and Python 3. Python 2とPython 3の両方をサポートします。


Installation (インストール)
==============================

``zaif`` is available on `PYPI <https://pypi.python.org/pypi>`_. Install with ``pip``:

.. code:: bash

    $ pip install zaif

or with ``easy_install``:

.. code:: bash

    $ easy_install zaif

The library is currently tested against Python versions 2.7 and 3.4+.

API Reference (APIリファレンス)
=================================

The official documentation can be found on the `Zaif API reference page <http://techbureau-api-document.readthedocs.io/ja/latest/index.html>`_.
公式のドキュメントは `Zaif APIのリファレンスページ <http://techbureau-api-document.readthedocs.io/ja/latest/index.html>`_ にあります。

Prerequisites (前提条件)
==============================

The first thing you need to do is to `Sign Up with Zaif <https://zaif.jp>`_.

Next, you need to obtain an **API Key** and an **API Secret**. If you're writing code for your own Zaif account, you can create API keys on `Zaif API Settings <https://zaif.jp/api_keys>`_ page. You can create multiple API keys with different permissions for your applications.

NOTE: Make sure to enable appropriate permissions for the API key.

Getting started (始める)
=============================

Create a ``Client`` object for interacting with the API:
APIと対話するための ``Client`` オブジェクトを作成します：

.. code:: python

    from zaif.client import Client

    api_key = 'your api key'
    api_secret = 'your api secret'

    client = Client(api_key,api_secret)

Error handling (エラー処理)
---------------------------------
All errors occurring during interaction with the API will be raised as exceptions. These exceptions will be subclasses of ``zaif.errors.ZaifError``.

* When the error involves the API server, the error raised will be a subclass of ``zaif.errors.APIServerError``. エラーがAPIサーバに関係する場合、発生したエラーは ``zaif.errors.APIServerError`` のサブクラスになります。
* When the error is associated with the response received form the API server, ``zaif.errors.APIResponseError`` will be raised. エラーがAPIサーバーから受信したレスポンスに関連付けられている場合、``zaif.errors.APIResponseError`` が発生します。

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

Usage (使い方)
-------------------
I've done my best to make the code clean, commented, and understandable; however it may not be exhaustive. For more details, please refer to the `Zaif API official documentation <http://techbureau-api-document.readthedocs.io/ja/latest/index.html>`_.

**In short**

- **Use args for URI paths**
- **Use kwargs for formData or query parameters**


**PUBLIC API (現物公開API)**

Get available currencies, tokens, ICO etc.
通貨情報を取得します。

.. code:: python

    client.get_currencies()
    client.get_currency('btc')
    client.get_currency('ETH') # capital for token currencies

Get currency pairs traded on the exchange.
通貨ペア情報を取得します。

.. code:: python

    client.get_currency_pairs()
    client.get_currency_pair('eth_btc')

Get current closing price for a currency pair.
現在の終値を取得します。

.. code:: python

    client.get_last_price('eth_btc')


Get ticker information for a currency pair.
ティッカーを取得します。

.. code:: python

    client.get_ticker('eth_btc')


Get trades for a currency pair.
全ての取引履歴を取得します。

.. code:: python

    client.get_trades('eth_btc')


Get board information (asks, bids) for a currency pair.
板情報を取得します。

.. code:: python

    client.get_depth('eth_btc')


**TRADING API (現物取引API)**

Get current balance (asset and token balances), API key permissions, number of past trades, number of open orders, server timestamp.
現在の残高（余力および残高・トークン）、APIキーの権限、過去のトレード数、アクティブな注文数、サーバーのタイムスタンプを取得します。

.. code:: python

    client.get_info()

It is a lightweight version of ``get_info()`` and returns items excluding past trades.
get_infoの軽量版で、過去のトレード数を除く項目を返します。

.. code:: python

    client.get_info2()

Get nickname and icon image path for your account.
チャットに使用されるニックネームと画像のパスを返します。

.. code:: python

    client.get_personal_info()

Get account information such as user ID, email, etc.
ユーザーIDやメールアドレスといった個人情報を取得します。

.. code:: python

    client.get_id_info()

Get trade history.
ユーザー自身の取引履歴を取得します。

.. code:: python

    client.get_trade_history()
    client.get_trade_history(currency_pair='eth_btc',count=10,order='ASC')


Get a list of active orders (currency pairs and tokens).
現在有効な注文一覧を取得します（未約定注文一覧）。

.. code:: python

    client.get_active_orders()
    client.get_active_orders(currency_pair='eth_btc')
    client.get_active_orders(is_token_both=True)


Create a new trading order.
取引注文を行います。

.. code:: python

    client.trade(currency_pair='eth_btc',
                 action='bid',
                 price=100,
                 amount=1.5)

    client.trade(currency_pair='eth_btc',
                 action='bid',
                 price=100,
                 amount=1.5,
                 limit=120)



Convenient function to create a buy order.

.. code:: python

    client.buy(currency_pair='eth_btc',price=100,amount=1.5)
    client.buy(currency_pair='eth_btc',price=100,amount=1.5,limit=120)

Convenient function to create a sell order.

.. code:: python

    client.sell(currency_pair='eth_btc',price=100,amount=1.5)
    client.sell(currency_pair='eth_btc',price=100,amount=1.5,limit=120)


Cancel an open order.
注文の取消しを行います。

.. code:: python

    client.cancel_order(order_id=123)
    client.cancel_order(order_id=123,currency_pair='eth_btc')


Withdraw currency to a specific address.
資金の引き出しリクエストを送信します。

.. code:: python

    client.withdraw(currency='ETH',address='0x1234abcd5678efgh',amount=1)


Get deposit payments (account funding) history for a currency.
入金履歴を取得します。

.. code:: python

    client.get_deposit_history(currency='btc')
    client.get_deposit_history(currency='ETH',count=50,order='ASC')


Get history of withdrawals for a currency.
出金履歴を取得します。

.. code:: python

    client.get_withdraw_history(currency='btc')
    client.get_withdraw_history(currency='ETH',count=50,sort='ASC')


**FUTURES API (先物公開API)**

Get information on all futures groups.
先物取引の情報を取得します。

.. code:: python

    client.get_groups()

Get information on a specific futures group

.. code:: python

    client.get_group(2)


Get current closing price of a specific futures group.
現在の終値を取得します。

.. code:: python

    client.get_group_last_price(2)


Get ticker for a futures group.
ティッカーを取得します。


.. code:: python

    client.get_group_ticker(2)

Get all trades of a futures group.
全ての取引履歴を取得します。

.. code:: python

    client.get_group_trades(2)

Get board information of a futures transaction.
板情報を取得します。

.. code:: python

    client.get_group_depth(2)


**LEVERAGE API (レバレッジ取引API)**

Get history of your leveraged trades.
レバレッジ取引のユーザー自身の取引履歴を取得します。

.. code:: python

    client.get_positions(type='futures',group_id=1)
    client.get_positions(type='futures',
                         group_id=1,
                         count=10,
                         order='ASC',
                         currency_pair='eth_btc')


Get detailed history of your leveraged trades.
レバレッジ取引のユーザー自身の取引履歴の明細を取得します。

.. code:: python

    client.get_position_history(type='futures',group_id=1,leverage_id=123)

Get currently valid order list of leveraged transactions.
レバレッジ取引の現在有効な注文一覧を取得します（未約定注文一覧）。

.. code:: python

    client.get_active_positions(type='futures',group_id=1)
    client.get_active_positions(type='futures',group_id=1,currency_pair='eth_btc')


Create a new leveraged transaction.
レバレッジ取引の注文を行います。

.. code:: python

    client.create_position(type='futures',
                           group_id=1,
                           currency_pair='eth_btc',
                           action='ask',
                           price=100.0,
                           amount=1,
                           leverage=3.25)
    client.create_position(type='futures',
                           group_id=1,
                           currency_pair='eth_btc',
                           action='ask',
                           price=100.0,
                           amount=1,
                           leverage=3.25,
                           limit=120,
                           stop=90)


Convenient method to create a new leveraged buy transaction.

.. code:: python

    client.create_buy_position(type='futures',
                               group_id=1,
                               currency_pair='eth_btc',
                               price=100.0,
                               amount=1,
                               leverage=3.25)
    client.create_buy_position(type='futures',
                               group_id=1,
                               currency_pair='eth_btc',
                               price=100.0,
                               amount=1,
                               leverage=3.25,
                               limit=120,
                               stop=90)

Convenient method to create a new leveraged sell transaction.

.. code:: python

    client.create_sell_position(type='futures',
                                group_id=1,
                                currency_pair='eth_btc',
                                price=100.0,
                                amount=1,
                                leverage=3.25)
    client.create_sell_position(type='futures',
                                group_id=1,
                                currency_pair='eth_btc',
                                price=100.0,
                                amount=1,
                                leverage=3.25,
                                limit=120,
                                stop=90)

Modify a leveraged transaction.
レバレッジ取引の注文の変更を行います。

.. code:: python

    client.change_position(type='margin',group_id=1,leverage_id=123)
    client.change_position(type='margin',group_id=1,leverage_id=123,limit=120)

Cancel a leveraged transaction.
レバレッジ取引の注文の取消しを行います。


.. code:: python

    client.cancel_position(type='margin',group_id=1,leverage_id=123)



Testing / Contributing (テスト/寄稿)
====================================
Any contribution is welcome! The process is simple:

* Fork this repo
* Make your changes
* Run the tests (for multiple versions: preferred)
* Submit a pull request.


Testing for your current python version (現在のPythonバージョン)
---------------------------------------------------------------------

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


Testing for multiple python versions (複数のPythonバージョン)
-------------------------------------------------------------------

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


License (ライセンス)
==========================

This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements (謝辞)
=========================

- `zaifapi <https://github.com/techbureau/zaifapi>`_

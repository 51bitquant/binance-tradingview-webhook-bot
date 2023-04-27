import requests
import time
import hmac
import hashlib
from threading import Lock
from datetime import datetime
from decimal import Decimal
import json

from .constant import RequestMethod, Interval, OrderSide, OrderType


class BinanceFutureHttpClient(object):

    def __init__(self, api_key=None, secret=None, timeout=5):
        self.key = api_key
        self.secret = secret
        self.host = "https://fapi.binance.com"
        self.recv_window = 5000
        self.timeout = timeout
        self.order_count_lock = Lock()
        self.order_count = 1_000_000

    def build_parameters(self, params: dict):
        keys = list(params.keys())
        keys.sort()
        return '&'.join([f"{key}={params[key]}" for key in params.keys()])

    def request(self, req_method: RequestMethod, path: str, requery_dict=None, verify=False):
        url = self.host + path

        if verify:
            query_str = self._sign(requery_dict)
            url += '?' + query_str
        elif requery_dict:
            url += '?' + self.build_parameters(requery_dict)
        headers = {"X-MBX-APIKEY": self.key}

        response = requests.request(req_method.value, url=url, headers=headers, timeout=self.timeout)
        if response.status_code == 200:
            return response.status_code, response.json()
        else:
            try:
                return response.status_code, json.loads(response.text)
            except Exception as error:
                return response.status_code, {"msg": response.text, 'error': str(error)}

    def server_time(self):
        path = '/fapi/v1/time'
        return self.request(req_method=RequestMethod.GET, path=path)

    def exchangeInfo(self):
        path = '/fapi/v1/exchangeInfo'
        return self.request(req_method=RequestMethod.GET, path=path)

    def order_book(self, symbol, limit=5):
        limits = [5, 10, 20, 50, 100, 500, 1000]
        if limit not in limits:
            limit = 5

        path = "/fapi/v1/depth"
        query_dict = {"symbol": symbol,
                      "limit": limit
                      }

        return self.request(RequestMethod.GET, path, query_dict)

    def get_kline(self, symbol, interval: Interval, start_time=None, end_time=None, limit=500):
        """

        :param symbol:
        :param interval:
        :param start_time:
        :param end_time:
        :param limit:
        :return:
        [
            1499040000000,      // 开盘时间
            "0.01634790",       // 开盘价
            "0.80000000",       // 最高价
            "0.01575800",       // 最低价
            "0.01577100",       // 收盘价(当前K线未结束的即为最新价)
            "148976.11427815",  // 成交量
            1499644799999,      // 收盘时间
            "2434.19055334",    // 成交额
            308,                // 成交笔数
            "1756.87402397",    // 主动买入成交量
            "28.46694368",      // 主动买入成交额
            "17928899.62484339" // 请忽略该参数
        ]
        """
        path = "/fapi/v1/klines"

        query_dict = {
            "symbol": symbol,
            "interval": interval.value,
            "limit": limit
        }

        if start_time:
            query_dict['startTime'] = start_time

        if end_time:
            query_dict['endTime'] = end_time

        return self.request(RequestMethod.GET, path, query_dict)

    def get_latest_price(self, symbol):
        path = "/fapi/v1/ticker/price"
        query_dict = {"symbol": symbol}
        return self.request(RequestMethod.GET, path, query_dict)

    def get_ticker(self, symbol):
        path = "/fapi/v1/ticker/bookTicker"
        query_dict = {"symbol": symbol}
        return self.request(RequestMethod.GET, path, query_dict)

    ########################### the following request is for private data ########################

    def _timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, params):

        requery_string = self.build_parameters(params)
        hexdigest = hmac.new(self.secret.encode('utf8'), requery_string.encode("utf-8"), hashlib.sha256).hexdigest()
        return requery_string + '&signature=' + str(hexdigest)

    def get_client_order_id(self):

        """
        generate the client_order_id for user.
        :return: new client order id
        """
        with self.order_count_lock:
            self.order_count += 1
            return "x-cLbi5uMH" + str(self._timestamp()) + str(self.order_count)

    def place_order(self, symbol: str, order_side: OrderSide, order_type: OrderType, quantity: Decimal, price: Decimal,
                    time_inforce="GTC", client_order_id=None, recvWindow=5000, stop_price=0):

        """
        下单..
        :param symbol: BTCUSDT
        :param side: BUY or SELL
        :param type: LIMIT MARKET STOP
        :param quantity: 数量.
        :param price: 价格
        :param stop_price: 停止单的价格.
        :param time_inforce:
        :param params: 其他参数

        LIMIT : timeInForce, quantity, price
        MARKET : quantity
        STOP: quantity, price, stopPrice
        :return:

        """

        path = '/fapi/v1/order'

        if client_order_id is None:
            client_order_id = self.get_client_order_id()

        params = {
            "symbol": symbol,
            "side": order_side.value,
            "type": 'LIMIT',
            "quantity": quantity,
            "price": price,
            "recvWindow": recvWindow,
            "timestamp": self._timestamp(),
            "newClientOrderId": client_order_id
        }

        if order_type == OrderType.LIMIT:
            params['type'] = 'LIMIT'
            params['timeInForce'] = time_inforce
        elif order_type == OrderType.MARKET:
            if params.get('price', None):
                del params['price']

        elif order_type == OrderType.MAKER:
            params['type'] = 'LIMIT'
            params['timeInForce'] = "GTX"

        elif order_type == OrderType.STOP:
            if stop_price > 0:
                params["stopPrice"] = stop_price
            else:
                raise ValueError("stopPrice must greater than 0")
        # print(params)
        return self.request(RequestMethod.POST, path=path, requery_dict=params, verify=True)

    def get_order(self, symbol, client_order_id=None):
        path = "/fapi/v1/order"
        query_dict = {"symbol": symbol, "timestamp": self._timestamp()}
        if client_order_id:
            query_dict["origClientOrderId"] = client_order_id

        return self.request(RequestMethod.GET, path, query_dict, verify=True)

    def cancel_order(self, symbol, client_order_id=None):
        path = "/fapi/v1/order"
        params = {"symbol": symbol, "timestamp": self._timestamp()}
        if client_order_id:
            params["origClientOrderId"] = client_order_id

        return self.request(RequestMethod.DELETE, path, params, verify=True)

    def get_open_orders(self, symbol=None):
        path = "/fapi/v1/openOrders"

        params = {"timestamp": self._timestamp()}
        if symbol:
            params["symbol"] = symbol

        return self.request(RequestMethod.GET, path, params, verify=True)

    def cancel_open_orders(self, symbol):
        """
        撤销某个交易对的所有挂单
        :param symbol: symbol
        :return: return a list of orders.
        """
        path = "/fapi/v1/allOpenOrders"

        params = {"timestamp": self._timestamp(),
                  "recvWindow": self.recv_window,
                  "symbol": symbol
                  }

        return self.request(RequestMethod.DELETE, path, params, verify=True)

    def get_balance(self):
        """
        [{'accountId': 18396, 'asset': 'USDT', 'balance': '530.21334791', 'withdrawAvailable': '530.21334791', 'updateTime': 1570330854015}]
        :return:
        """
        path = "/fapi/v1/balance"
        params = {"timestamp": self._timestamp()}

        return self.request(RequestMethod.GET, path=path, requery_dict=params, verify=True)

    def get_account_info(self):
        """
        {'feeTier': 2, 'canTrade': True, 'canDeposit': True, 'canWithdraw': True, 'updateTime': 0, 'totalInitialMargin': '0.00000000',
        'totalMaintMargin': '0.00000000', 'totalWalletBalance': '530.21334791', 'totalUnrealizedProfit': '0.00000000',
        'totalMarginBalance': '530.21334791', 'totalPositionInitialMargin': '0.00000000', 'totalOpenOrderInitialMargin': '0.00000000',
        'maxWithdrawAmount': '530.2133479100000', 'assets':
        [{'asset': 'USDT', 'walletBalance': '530.21334791', 'unrealizedProfit': '0.00000000', 'marginBalance': '530.21334791',
        'maintMargin': '0.00000000', 'initialMargin': '0.00000000', 'positionInitialMargin': '0.00000000', 'openOrderInitialMargin': '0.00000000',
        'maxWithdrawAmount': '530.2133479100000'}]}
        :return:
        """
        path = "/fapi/v1/account"
        params = {"timestamp": self._timestamp()}
        return self.request(RequestMethod.GET, path, params, verify=True)

    def get_position_info(self, symbol):
        """
        [{'symbol': 'BTCUSDT', 'positionAmt': '0.000', 'entryPrice': '0.00000', 'markPrice': '8326.40833498', 'unRealizedProfit': '0.00000000', 'liquidationPrice': '0'}]
        :return:

        if the symbol is not None, then return the following values:
        [{'symbol': 'ETHUSDT', 'positionAmt': '0.000', 'entryPrice': '0.0', 'markPrice': '3024.93000000',
        'unRealizedProfit': '0.00000000', 'liquidationPrice': '0', 'leverage': '25', 'maxNotionalValue': '1500000',
        'marginType': 'cross', 'isolatedMargin': '0.00000000', 'isAutoAddMargin': 'false', 'positionSide': 'BOTH',
        'notional': '0', 'isolatedWallet': '0', 'updateTime': 1649066944718}]
        """
        path = "/fapi/v2/positionRisk"
        params = {"timestamp": self._timestamp()}
        if symbol:
            params['symbol'] = symbol

        return self.request(RequestMethod.GET, path, params, verify=True)

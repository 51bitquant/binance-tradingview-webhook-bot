import json, config
from flask import Flask, request
from api.binance_spot import BinanceSpotHttpClient
from api.binance_future import BinanceFutureHttpClient, OrderSide, OrderType
from event import EventEngine, Event, EVENT_TIMER, EVENT_SIGNAL
import time
from decimal import Decimal

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    return "Hello Flask, This is for testing."


@app.route('/webhook', methods=['POST', "GET"])
def webhook():
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return "failure"

    event = Event(EVENT_SIGNAL, data=data)
    event_engine.put(event)

    return "success"


def trade(symbol, action, vol, data):
    if action == 'exit':

        if vol > 0:
            vol1 = str(vol)
            binance_future_client.place_order(
                symbol=symbol,
                order_side=OrderSide.SELL,
                order_type=OrderType.MARKET,
                quantity=Decimal(vol1),
                price=Decimal(str(data['price']))
            )

        elif vol < 0:

            vol1 = str(abs(vol))
            binance_future_client.place_order(
                symbol=symbol,
                order_side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=Decimal(vol1),
                price=Decimal(str(data['price']))
            )

    elif action == 'long':

        if vol < 0:
            vol1 = str(abs(vol * 2))
            binance_future_client.place_order(
                symbol=symbol,
                order_side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=Decimal(vol1),
                price=Decimal(str(data['price']))
            )

        if vol == 0:
            # config your trading volume in config.py
            vol1 = config.SYMBOL_INFO.get(symbol, {}).get('trading_volume', 0.002)
            binance_future_client.place_order(
                symbol=symbol,
                order_side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=Decimal(str(vol1)),
                price=Decimal(str(data['price']))
            )


    elif action == 'short':
        if vol > 0:
            vol1 = str(abs(vol * 2))
            binance_future_client.place_order(
                symbol=symbol,
                order_side=OrderSide.SELL,
                order_type=OrderType.MARKET,
                quantity=Decimal(vol1),
                price=Decimal(str(data['price']))
            )

        if vol == 0:
            vol1 = config.SYMBOL_INFO.get(symbol, {}).get('trading_volume', 0.002)
            binance_future_client.place_order(
                symbol=symbol,
                order_side=OrderSide.SELL,
                order_type=OrderType.MARKET,
                quantity=Decimal(str(vol1)),
                price=Decimal(str(data['price']))
            )


def timer_event(event: Event):
    for key in future_signal_dict.keys():
        data = future_signal_dict[key]

        symbol = data['symbol']
        action = data['action']

        binance_future_client.cancel_open_orders(symbol)
        pos_infos = binance_future_client.get_position_info(symbol)

        if isinstance(pos_infos, list) and len(pos_infos) == 1:
            pos = pos_infos[0]
            vol = float(pos.get('positionAmt', 0))

            trade(symbol, action, vol, data)

    for key in spot_signal_dict.keys():
        """
        check your spot signal here, whether your buy/sell order filled.
        """
        pass


def signal_event(event: Event):
    """
    :param event: the event that contains the signal data
    the signal data like below.
    {'action': 'long',
    'symbol': 'ETHUSDT', 'exchange': 'binance_future',
    'price': '3054.66', 'close': '3054.66',
    'passphrase': 'yerongcun02'}

    :return: None
    """
    data = event.data
    symbol = data['symbol']
    action = data['action']

    if data['exchange'] == 'binance_future':
        future_signal_dict[symbol] = data
        pos_infos = binance_future_client.get_position_info(symbol)

        """
        [{'symbol': 'ETHUSDT', 'positionAmt': '0.000', 'entryPrice': '0.0', 'markPrice': '3024.93000000', 
        'unRealizedProfit': '0.00000000', 'liquidationPrice': '0', 'leverage': '25', 'maxNotionalValue': '1500000', 
        'marginType': 'cross', 'isolatedMargin': '0.00000000', 'isAutoAddMargin': 'false', 'positionSide': 'BOTH', 
        'notional': '0', 'isolatedWallet': '0', 'updateTime': 1649066944718}]
        """
        if isinstance(pos_infos, list) and len(pos_infos) == 1:
            pos = pos_infos[0]
            vol = float(pos.get('positionAmt', 0))
            trade(symbol, action, vol, data)

    elif data['exchange'] == 'binance_spot':
        spot_signal_dict[symbol] = data
        # write your logic code here.


if __name__ == '__main__':
    future_signal_dict = {}
    spot_signal_dict = {}

    binance_spot_client = BinanceSpotHttpClient(api_key=config.API_KEY, secret=config.API_SECRET, try_counts=1)
    binance_future_client = BinanceFutureHttpClient(api_key=config.API_KEY, secret=config.API_SECRET, try_counts=1)

    event_engine = EventEngine(interval=30)
    event_engine.start()
    event_engine.register(EVENT_TIMER, timer_event)
    event_engine.register(EVENT_SIGNAL, signal_event)

    app.run(host='127.0.0.1', port=8888, debug=False)

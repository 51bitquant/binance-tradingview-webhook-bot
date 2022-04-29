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


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = json.loads(request.data)
        print(data)
        if data.get('passphrase', None) != config.WEBHOOK_PASSPHRASE:
            return "failure"

        # here insert your code here.
        # replace your placing order code here, you can refer to the main.py to see how to place order.

        return "success"
    except Exception as error:
        print(f"error: {error}")
        return "failure"



def timer_event(event: Event):
    pass
    # this is the timer loop, you can do something interval.




if __name__ == '__main__':

    binance_spot_client = BinanceSpotHttpClient(api_key=config.API_KEY, secret=config.API_SECRET)
    binance_future_client = BinanceFutureHttpClient(api_key=config.API_KEY, secret=config.API_SECRET)

    event_engine = EventEngine(interval=15)  # you can update the loop interval.
    event_engine.start()
    event_engine.register(EVENT_TIMER, timer_event)

    app.run(host='127.0.0.1', port=8888, debug=False)

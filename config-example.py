WEBHOOK_PASSPHRASE = "your webhook passphrase"
API_KEY = 'past your api secret here.'
API_SECRET = 'past your api secret here.'

# config your the symbol you want to trade here. tick_price is the price's precision, min_volume is the volume's precision.
# pls check out the price's precision and volume's precision from Binance Exchange.
SYMBOL_INFO = {
    "BTCUSDT": {'tick_price': 0.1,
                'min_volume': 0.001,
                'trading_volume': 0.1
                },

    "ETHUSDT": {'tick_price': 0.01,
                'min_volume': 0.001,
                'trading_volume': 0.002
                }
}

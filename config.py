# the following is the configuration for your tradingview webhook bot

WEBHOOK_PASSPHRASE = "your password like"   # the password for security, must be the same from tradingview webhook settings.
API_KEY = 'past your api secret here.'
API_SECRET = 'past your api secret here.'


# config your strategy name and the strategy data you want to trade here
#  tick_price is the price's precision
#  min_volume is the volume's precision.
#  trading_volume is the amount of order you want to place here.
#  symbol is the binance symbol.
#  pos is the strategy's position
# pls check out the price's precision and volume's precision from Binance Exchange.

strategies = {
    # strategy name -> strategy data
    "BTCUSDT_1h":  {'tick_price': 0.1,
                   'min_volume': 0.001,
                   'trading_volume': 0,
                   'symbol': 'BTCUSDT',
                    'pos': 0   # current position when start your strategy.
                   },

    "ETHUSDT_5min":  {'tick_price': 0.01,
                     'min_volume': 0.001,
                     'trading_volume': 0,
                     'symbol': 'ETHUSDT',
                      'pos': 0   # current position when start your strategy.
                     },

    "ETHUSDT_15min": {'tick_price': 0.01,
                      'min_volume': 0.001,
                      'trading_volume': 0,
                      'symbol': 'ETHUSDT',
                      'pos': 0  # current position when start your strategy.
                      },

    "UNIUSDT_5min":  {'tick_price': 0.01,
                     'min_volume': 0.001,
                     'trading_volume': 0,
                     'symbol': 'UNIUSDT',
                      'pos': 0  # current position when start your strategy.
                     },

    "UNIUSDT_15min": {'tick_price': 0.01,
                      'min_volume': 0.001,
                      'trading_volume': 0,
                      'symbol': 'UNIUSDT',
                      'pos': 0  # current position when start your strategy.
                      },

}

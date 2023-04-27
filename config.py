# the following is the configuration for your tradingview webhook bot

# WEBHOOK_PASSPHRASE = "your password like"   # the password for security, must be the same from tradingview webhook settings.
# API_KEY = 'past your api secret here.'
# API_SECRET = 'past your api secret here.'

# the passphrase is a string for verifying that prevents others(especially the bad guy) to invoke the POST request in the program.
# passphrase 字符串是为了验证防止其他人(特别是坏人)去调用你的POST请求接口，这个接口是可以发送下单信号的。

WEBHOOK_PASSPHRASE = "setting your tradingview passphrase, it's not your tradingview password."
API_KEY = 'binance exchange api key, remember to edit restriction'
API_SECRET = 'api secret'

CANCEL_ORDER_IN_SECONDS = 60 # every X second, will cancel your order

# config your strategy name and the strategy data you want to trade here
#  tick_price: the price's precision, in Decimal
#  min_volume: the volume's precision, in Decimal
#  trading_volume: the amount of order you want to place here.
#  symbol: the binance symbol.
#  pos is the strategy's position in Decimal
# pls check out the price's precision and volume's precision from Binance Exchange.
from decimal import Decimal

# the amount should be wrapped with Decimal, or your order amount precision will be incorrect.
# 数量应该使用Decimal类来包裹起来，防止下单数量，价格精度的丢失。
#

strategies = {
    # strategy name -> strategy data
    "BTCUSDT_1h": {
        'symbol': 'BTCUSDT',
        'tick_price': Decimal("0.1"),
        'min_volume': Decimal("0.001"),
        'trading_volume': Decimal("0"),  # 设置为你交易的数量，用Decimal表示.
        'pos': Decimal("0")  # current position when start your strategy, 策略当前的仓位, 用Decimal表示
    },
    "ETHBUSD_5min": {
        'symbol': 'ETHBUSD',
        'tick_price': Decimal("0.01"),
        'min_volume': Decimal("0.001"),
        'trading_volume': Decimal("0.01"),
        'pos': Decimal("0")  # current position when start your strategy.
    },
    "ETHUSDT_15min": {
        'symbol': 'ETHUSDT',
        'tick_price': Decimal("0.01"),
        'min_volume': Decimal("0.001"),
        'trading_volume': Decimal("0.01"),
        'pos': Decimal("0")  # current position when start your strategy.
    },
    "UNIUSDT_5min": {
        'symbol': 'UNIUSDT',
        'tick_price': Decimal("0.01"),
        'min_volume': Decimal("0.001"),
        'trading_volume': Decimal("100"),
        'pos': Decimal("0")  # current position when start your strategy.
    },
    "UNIUSDT_15min": {
        'symbol': 'UNIUSDT',
        'tick_price': Decimal("0.01"),
        'min_volume': Decimal("0.001"),
        'trading_volume': Decimal("1000"),
        'pos': Decimal("0")  # current position when start your strategy.
    },

}

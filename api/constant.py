from enum import Enum

class OrderStatus(object):
    """
    Order Status
    """
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    PENDING_CANCEL = "PENDING_CANCEL"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class OrderType(Enum):
    """
    Order type
    """
    LIMIT = "LIMIT"  # Limit order 现价单
    MARKET = "MARKET" # 市价单 吃单
    STOP = "STOP" #
    MAKER = "MAKER"  # 做市单 Maker order, POST Only.


class RequestMethod(Enum):
    """
    Request methods
    """
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Interval(Enum):
    """
    Interval for klines
    """
    MINUTE_1 = '1m'
    MINUTE_3 = '3m'
    MINUTE_5 = '5m'
    MINUTE_15 = '15m'
    MINUTE_30 = '30m'
    HOUR_1 = '1h'
    HOUR_2 = '2h'
    HOUR_4 = '4h'
    HOUR_6 = '6h'
    HOUR_8 = '8h'
    HOUR_12 = '12h'
    DAY_1 = '1d'
    DAY_3 = '3d'
    WEEK_1 = '1w'
    MONTH_1 = '1M'


class OrderSide(Enum):
    """
    order side
    """
    BUY = "BUY"
    SELL = "SELL"


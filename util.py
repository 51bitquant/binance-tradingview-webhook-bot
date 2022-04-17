from decimal import Decimal, ROUND_DOWN


def round_to(value: float, target: Decimal) -> Decimal:
    """
    Round price to price tick value.
    """
    value = Decimal(str(value))
    rounded = value.quantize(target)

    return rounded


def floor_to(value: float, target: Decimal) -> Decimal:
    """
    Similar to math.floor function, but to target float number.
    """
    value = Decimal(str(value))
    result = value.quantize(target, rounding=ROUND_DOWN)

    return result

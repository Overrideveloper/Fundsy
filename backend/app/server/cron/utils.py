from decimal import Decimal

def calculateDailyAppreciation(amount: int, rate: int, duration: int) -> Decimal:
    duration_in_days = int(duration/86400)
    return Decimal((rate * amount)/(100 * duration_in_days))

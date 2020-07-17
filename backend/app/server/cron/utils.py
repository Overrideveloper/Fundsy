def calculate_daily_appreciation(amount: int, rate: int, duration: int) -> int:
    duration_in_days = int(duration/86400)
    return (rate * amount)/(100 * duration_in_days)

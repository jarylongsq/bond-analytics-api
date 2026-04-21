from datetime import date

def day_count_discount(
    day_count: str,
    settlement_dt: date,
    prev_cpn_dt: date,
    next_cpn_dt: date
):
    if day_count == "30/360":
        d1, m1, y1 = prev_cpn_dt.day, prev_cpn_dt.month, prev_cpn_dt.year
        d2, m2, y2 = next_cpn_dt.day, next_cpn_dt.month, next_cpn_dt.year
        num_days_btw_cpn_dt = (y2 - y1)*360 + (m2 - m1)*30 + (d2 - d1)

        d1, m1, y1 = settlement_dt.day, settlement_dt.month, settlement_dt.year
        d2, m2, y2 = next_cpn_dt.day, next_cpn_dt.month, next_cpn_dt.year
        settle_to_next_coupon = (y2 - y1)*360 + (m2 - m1)*30 + (d2 - d1)
    else:
        num_days_btw_cpn_dt = (next_cpn_dt - prev_cpn_dt).days
        settle_to_next_coupon = (next_cpn_dt - settlement_dt).days

    return settle_to_next_coupon, num_days_btw_cpn_dt 
    
def calculate_bond_price(
    coupon: float,
    redemption_value: float,
    maturity: float,
    cpn_freq: int,
    yield_per_period: float,
    settlement_dt:date,
    day_count: str,
    prev_cpn_dt: date,
    next_cpn_dt: date
) -> float:
    """
    Used to calculate the dirty price of a bond via discounting the cashflows (coupon periods + redemption)
    """
    num_cpn_period: int = cpn_freq * maturity
    settle_to_next_coupon, num_days_btw_cpn_dt = day_count_discount(day_count, settlement_dt, prev_cpn_dt, next_cpn_dt)
    w = settle_to_next_coupon / num_days_btw_cpn_dt
    dirty_price = 0
    for i in range(1, num_cpn_period + 1):
        if i == num_cpn_period:
            dirty_price += redemption_value / (1 + yield_per_period/100) ** (i-1 + w)
        dirty_price += coupon / (1 + yield_per_period/100) ** (i-1 + w)
    return dirty_price

def calculate_accrued_interest(
    coupon: float,
    cpn_freq: int,
    day_count: str,
    settlement_dt: date,
    prev_cpn_dt: date,
    next_cpn_dt: date    
) -> float:
    settle_to_next_coupon, num_days_btw_cpn_dt = day_count_discount(day_count, settlement_dt, prev_cpn_dt, next_cpn_dt)
    accrued_interest = (num_days_btw_cpn_dt - settle_to_next_coupon) / num_days_btw_cpn_dt * coupon / cpn_freq
    return accrued_interest
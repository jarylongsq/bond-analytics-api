from pydantic import BaseModel
from datetime import date

class BondPriceRequest(BaseModel):
    coupon: float
    redemption_value: float
    maturity: float
    cpn_freq: int
    yield_per_period: float
    settlement_dt:date
    day_count: str
    prev_cpn_dt: date
    next_cpn_dt: date

class BondPriceResponse(BaseModel):
    clean_price: float
    accrued_interest: float
    dirty_price: float
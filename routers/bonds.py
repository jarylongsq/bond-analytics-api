from fastapi import APIRouter
from models.bonds import BondPriceRequest, BondPriceResponse
from services.analytics import calculate_bond_price, calculate_accrued_interest

# Every endpoint will have /bonds prepended to it 
router = APIRouter(prefix="/bonds", tags=["bonds"])

# Post method calling bonds/price will cause this function to run
@router.post("/price")
def get_bond_price(request: BondPriceRequest) -> BondPriceResponse:
    clean_price = calculate_bond_price(
        coupon = request.coupon,
        redemption_value = request.redemption_value,
        maturity = request.maturity,
        cpn_freq = request.cpn_freq,
        yield_per_period = request.yield_per_period,
        settlement_dt = request.settlement_dt,
        day_count = request.day_count,
        prev_cpn_dt = request.prev_cpn_dt,
        next_cpn_dt = request.next_cpn_dt,
    )
    accrued_interest = calculate_accrued_interest(
        coupon = request.coupon,
        cpn_freq = request.cpn_freq,
        settlement_dt = request.settlement_dt,
        day_count = request.day_count,
        prev_cpn_dt = request.prev_cpn_dt,
        next_cpn_dt = request.next_cpn_dt  
    )
    
    dirty_price = clean_price + accrued_interest

    return BondPriceResponse(
        clean_price = clean_price,
        accrued_interest = accrued_interest,
        dirty_price = dirty_price
    )
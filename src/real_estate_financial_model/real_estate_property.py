from typing import List, Dict, Optional


class RealEstateProperty:
    def __init__(self,
                 purchase_price: int,
                 monthly_rent_income: int,
                 square_meters: int,
                 parking_spots: int = 0,
                 warehouse: bool = False,
                 balcony_square_meter: int = 0,
                 after_repair_value: Optional[int] = None,
                 annual_appreciation_percentage: float = 0.0
                 ):
        self.purchase_price = purchase_price
        self.square_meters = square_meters
        self.parking_spots = parking_spots
        self.warehouse = warehouse
        self.monthly_rent_income = monthly_rent_income
        self.balcony_square_meter = balcony_square_meter
        self.after_repair_value = purchase_price if after_repair_value is None else after_repair_value
        self.annual_appreciation_percentage = annual_appreciation_percentage

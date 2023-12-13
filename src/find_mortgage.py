from typing import Optional
from src.investors.real_estate_investors_portfolio import RealEstateInvestorsPortfolio


class FindMortgage():
    def __init__(self, real_estate_investors_portfolio: RealEstateInvestorsPortfolio, property_value: int,
                 mortgage_amount: Optional[int] = None, loan_to_value: Optional[float] = None, exit_after: int = None):
        self.real_estate_investors_portfolio = real_estate_investors_portfolio
        self.exit_after = exit_after
        if mortgage_amount is None and loan_to_value is None:
            raise ValueError(
                "Please provide values for either mortgage_amount or loan_to_value. Both parameters cannot be None.")
        if mortgage_amount is not None \
                and loan_to_value is not None \
                and mortgage_amount != round(property_value * loan_to_value):
            raise ValueError(
                "Mismatch in mortgage amount calculation. Please ensure that mortgage_amount is correctly calculated based on the given loan_to_value and property_value.")
        if mortgage_amount is None and loan_to_value is not None:
            mortgage_amount = round(property_value * loan_to_value)
        if loan_to_value is None:
            loan_to_value = round(mortgage_amount / property_value, 2)
        if property_value > real_estate_investors_portfolio.calculate_maximum_property_price():
            raise ValueError(
                "Property value exceeds the maximum allowed value. Please adjust the property value accordingly.")
        if mortgage_amount > real_estate_investors_portfolio.calculate_maximum_loan_amount():
            raise ValueError(
                "Mortgage amount exceeds the maximum allowed loan amount. Please adjust the mortgage amount accordingly.")

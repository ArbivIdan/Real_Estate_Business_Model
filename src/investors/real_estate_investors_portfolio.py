from src.investors.real_estate_investment_type import RealEstateInvestmentType
from src.investors.real_estate_investor import RealEstateInvestor
import numpy_financial as npf
from src.mortgage_utils.mortgage_financial_utils import calculate_maximum_loan_amount
from src.investors.real_estate_investment_type import RealEstateInvestmentType
from typing import Optional


class RealEstateInvestorsPortfolio:
    def __init__(self, *real_estate_investor: RealEstateInvestor):

        self.investors = list(real_estate_investor)
        self.num_borrowers = (len(self.investors))

    def calculate_disposable_income(self):
        return sum([investor.disposable_income for investor in self.investors])

    def calculate_monthly_total_debt_payment(self):
        return sum([investor.total_debt_payment for investor in self.investors])

    def calculate_annual_total_debt_payment(self):
        return 12 * self.calculate_monthly_total_debt_payment()

    def calculate_monthly_total_net_income(self):
        return sum([investor.net_monthly_income for investor in self.investors])

    def calculate_annual_total_net_income(self):
        return 12 * self.calculate_monthly_total_debt_payment()

    def calculate_maximum_monthly_loan_repayment(self):
        return sum([investor.maximum_monthly_loan_repayment for investor in self.investors])

    def calculate_total_available_equity(self):
        return sum([investor.total_available_equity for investor in self.investors])

    def calculate_maximum_loan_amount(self, monthly_payment: Optional[int] = None, num_payments: int = 360):
        if monthly_payment is None:
            monthly_payment = self.calculate_maximum_monthly_loan_repayment()
        maximum_monthly_loan_repayment = self.calculate_maximum_monthly_loan_repayment()
        if monthly_payment > maximum_monthly_loan_repayment:
            assert False, f"Monthly payment '{monthly_payment}' exceeds the maximum allowable monthly loan repayment '{maximum_monthly_loan_repayment}'."
        return calculate_maximum_loan_amount(num_payments, monthly_payment)

    def get_investors_purchase_taxes_type(self):
        #TODO
        return RealEstateInvestmentType.SingleApartment

    def get_investors_selling_taxes_type(self):
        #TODO
        return RealEstateInvestmentType.SingleApartment

    def get_gross_rental_income(self):
        return sum([investor.gross_rental_income for investor in self.investors])

    def calculate_maximum_property_price(self):
        # TODO: check how multiple ppl take loans works
        max_possible_ltv = min([investor.real_estate_invest_type.value for investor in self.investors])
        total_available_equity = self.calculate_total_available_equity()
        maximum_property_price = total_available_equity / (1 - max_possible_ltv)
        loan_needed = maximum_property_price - total_available_equity
        if loan_needed > self.calculate_maximum_loan_amount():
            maximum_property_price = total_available_equity + self.calculate_maximum_loan_amount()
        return maximum_property_price

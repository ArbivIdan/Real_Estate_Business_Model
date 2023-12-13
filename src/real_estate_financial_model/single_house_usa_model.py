from src.real_estate_financial_model.real_estate_financial_utils import debt_service_coverage_ratio, debt_to_income
from src.real_estate_financial_model.single_house_model import SingleHouseModel
from abc import ABC


class SingleHouseUSAModel(SingleHouseModel, ABC):
    def calculate_dscr(self) -> float:
        # Debt Service Coverage Ratio
        # Annual NOI / Annual Debt Service (Principal + Interest)
        return debt_service_coverage_ratio(net_operating_income=self.calculate_annual_noi(),
                                           annual_loan_payment=self.mortgage.get_annual_payments())

    def calculate_dti(self) -> float:
        # Debt to income
        # Total Annual Debt Payments / Gross Annual Income
        annual_debt_payments = [payment + self.investors_portfolio.calculate_annual_total_debt_payment() for payment in
                                self.mortgage.get_annual_payments()]
        annual_income = self.calculate_annual_rent_income() + self.investors_portfolio.calculate_annual_total_net_income()
        return round(debt_to_income(annual_debt_payments, annual_income), 2)

    def calculate_broker_purchase_cost(self):
        #TODO: check how brokers paid in USA
        pass


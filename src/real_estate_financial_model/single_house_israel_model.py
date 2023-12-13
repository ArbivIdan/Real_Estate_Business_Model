from typing import List

from src.investors.real_estate_investment_type import RealEstateInvestmentType
from src.real_estate_financial_model.single_house_model import SingleHouseModel
from abc import ABC, abstractmethod
PURCHASE_TAX_DIC = {
    RealEstateInvestmentType.SingleApartment: 0,
    RealEstateInvestmentType.AlternativeApartment: 0.08,
    RealEstateInvestmentType.AdditionalApartment: 0.08
}

SELLING_TAX_DIC = {
    RealEstateInvestmentType.SingleApartment: 0,
    RealEstateInvestmentType.AlternativeApartment: 0,
    RealEstateInvestmentType.AdditionalApartment: 0.25
}

class SingleHouseIsraelModel(SingleHouseModel, ABC):

    def calculate_broker_purchase_cost(self):
        return round(self.broker_purchase_percentage * self.real_estate_property.purchase_price)

    def calculate_closing_costs(self) -> int:
        return self.calculate_purchase_additional_transactions_cost() + \
               self.calculate_total_renovation_expenses() + \
               self.mortgage_advisor_cost + \
               self.appraiser_cost + \
               self.calculate_broker_purchase_cost() + \
               self.furniture_cost + \
               self.escort_costs + \
               self.lawyer_cost + \
               self.calculate_purchase_tax()

    def calculate_purchase_tax(self) -> int:
        return round(PURCHASE_TAX_DIC[
                         self.investors_portfolio.get_investors_purchase_taxes_type()] * self.real_estate_property.purchase_price)

    def calculate_monthly_rental_property_taxes(self) -> int:
        should_pay_rental_taxes = self.investors_portfolio.get_gross_rental_income() + self.real_estate_property.monthly_rent_income > 5000
        return round(0.1 * self.real_estate_property.monthly_rent_income) if should_pay_rental_taxes else 0

    def calculate_capital_gain_tax(self) -> int:
        tax_percentage = SELLING_TAX_DIC[self.investors_portfolio.get_investors_selling_taxes_type()]
        return self.estimate_sale_price() * tax_percentage

    def calculate_annual_insurances_expenses(self) -> int:
        return self.annual_house_insurance_cost + self.annual_life_insurance_cost

    def calculate_monthly_operating_expenses(self) -> int:
        return self.calculate_monthly_vacancy_cost() + \
               self.calculate_monthly_maintenance_and_repairs() + \
               self.calculate_monthly_insurances_expenses() + \
               self.calculate_monthly_rental_property_taxes() + \
               self.calculate_monthly_property_management_fees()

    def calculate_selling_expenses(self) -> int:
        # TODO - add more selling expenses
        return round(self.broker_sell_percentage * self.estimate_sale_price())

    @abstractmethod
    def calculate_total_expenses(self) -> int:
        pass

    @abstractmethod
    def calculate_annual_expenses_distribution(self) -> List[float]:
        pass
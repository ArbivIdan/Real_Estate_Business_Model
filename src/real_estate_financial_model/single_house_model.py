from typing import Dict, Optional, List, Tuple, Union

import matplotlib.pyplot as plt
import matplotlib
from src.investors.real_estate_investors_portfolio import RealEstateInvestorsPortfolio
from src.investors.real_estate_investment_type import RealEstateInvestmentType
from src.mortgage_pipeline import MortgagePipeline
import numpy as np
import numpy_financial as npf
from real_estate_property import RealEstateProperty
from src.mortgage_tracks.constant_not_linked import ConstantNotLinked
from src.mortgage_tracks.mortgage_track import MortgageTrack
from src.investors.real_estate_investor import RealEstateInvestor
from src.real_estate_financial_model.real_estate_financial_utils import gross_yield, \
    debt_service_coverage_ratio, debt_to_income, loan_to_cost, loan_to_value, cash_of_cash, return_on_investment, noi, \
    cap_rate
from abc import ABC, abstractmethod

matplotlib.use('TkAgg')


class SingleHouseModel(ABC):

    def __init__(self,
                 investors_portfolio: RealEstateInvestorsPortfolio,
                 mortgage: MortgagePipeline,
                 real_estate_property: RealEstateProperty,
                 years_to_exit: int = 30,
                 average_interest_in_exit: Optional[Dict[MortgageTrack.__class__, float]] = None,
                 mortgage_advisor_cost: int = 0,
                 appraiser_cost: int = 0,
                 lawyer_cost: int = 0,
                 escort_costs: int = 0,
                 additional_transaction_costs_dic: Union[int, Dict[str, int]] = 0,
                 renovation_expenses_dic: Union[int, Dict[str, int]] = 0,
                 furniture_cost: int = 0,
                 broker_purchase_percentage: float = 0.0,
                 broker_rent_percentage: float = 0.0,
                 broker_sell_percentage: float = 0.0,
                 vacancy_percentage: float = 0.0,
                 annual_maintenance_cost_percentage: float = 0.0,
                 annual_life_insurance_cost: int = 0,
                 annual_house_insurance_cost: int = 0,
                 construction_input_index_annual_growth: int = 0,
                 equity_required_by_percentage: float = 0.25,
                 years_until_key_reception: int = 0,
                 contractor_payment_distribution: List[float] = 0,
                 management_fees_percentage: int = 0
                 ):
        # Required Parameters
        self.investors_portfolio = investors_portfolio
        self.mortgage = mortgage
        self.real_estate_property = real_estate_property

        # Optional Parameters
        self.years_to_exit = years_to_exit
        self.average_interest_in_exit = average_interest_in_exit
        self.mortgage_advisor_cost = mortgage_advisor_cost
        self.appraiser_cost = appraiser_cost
        self.lawyer_cost = lawyer_cost
        self.escort_costs = escort_costs
        self.broker_purchase_percentage = broker_purchase_percentage
        self.broker_rent_percentage = broker_rent_percentage
        self.broker_sell_percentage = broker_sell_percentage
        self.vacancy_percentage = vacancy_percentage
        self.annual_maintenance_cost_percentage = annual_maintenance_cost_percentage
        self.annual_life_insurance_cost = annual_life_insurance_cost
        self.annual_house_insurance_cost = annual_house_insurance_cost
        # self.construction_input_index_annual_growth = construction_input_index_annual_growth
        self.equity_required_by_percentage = equity_required_by_percentage
        # self.years_until_key_reception = years_until_key_reception
        # self.contractor_payment_distribution = contractor_payment_distribution
        self.furniture_cost = furniture_cost
        self.additional_transaction_costs_dic = additional_transaction_costs_dic
        self.renovation_expenses = renovation_expenses_dic
        self.management_fees_percentage = management_fees_percentage

    def validate_parameters(self):
        # TODO
        pass

    # Financial Metrics and Calculations

    def calculate_loan_to_cost(self) -> float:
        return round(loan_to_cost(loan_amount=self.mortgage.total_initial_loan_amount,
                                  total_project_cost=self.real_estate_property.purchase_price), 2)

    def calculate_loan_to_value(self) -> float:
        return loan_to_value(loan_amount=self.mortgage.total_initial_loan_amount,
                             after_repair_value=self.real_estate_property.after_repair_value)

    def calculate_net_monthly_cash_flow(self) -> int:
        # This method assumes the interest is constant
        monthly_revenues = self.real_estate_property.monthly_rent_income
        print(f"Monthly revenues: {monthly_revenues}")
        monthly_expenses = self.calculate_monthly_operating_expenses() + self.mortgage.calculate_initial_monthly_payment()
        print(f"monthly_expenses: {monthly_expenses}")
        return monthly_revenues - monthly_expenses

    def calculate_net_annual_cash_flow(self) -> int:
        return 12 * self.calculate_net_monthly_cash_flow()

    def calculate_cash_on_cash(self) -> float:
        return cash_of_cash(net_annual_cash_flow=self.calculate_net_annual_cash_flow(),
                            total_equity_needed_for_purchase=self.calculate_total_equity_needed_for_purchase())

    def calculate_annual_irr(self):
        annual_cash_flow_distribution = self.calculate_annual_cash_flow_distribution()
        return round(100 * npf.irr(annual_cash_flow_distribution), 2)

    def calculate_annual_cash_flow_distribution(self):
        annual_revenue_distribution = self.calculate_annual_revenue_distribution()
        annual_expenses_distribution = self.calculate_annual_expenses_distribution()
        annual_cash_flow_distribution = [a - b for a, b in
                                         zip(annual_revenue_distribution, annual_expenses_distribution)]
        return annual_cash_flow_distribution

    def calculate_roi(self) -> float:
        # Return on investment
        # Net Profit / Cost Of Investment
        return return_on_investment(net_profit=self.calculate_net_profit(),
                                    total_equity_needed_for_purchase=self.calculate_total_equity_needed_for_purchase())

    def calculate_monthly_noi(self):
        # Net Operating Income
        # (Operating Income - Operating Expenses)
        return noi(operating_income=self.real_estate_property.monthly_rent_income,
                   operating_expenses=self.calculate_monthly_operating_expenses())

    def calculate_annual_noi(self):
        return 12 * self.calculate_monthly_noi()

    def calculate_annual_cap_rate(self):
        # NOI / Current Market Value or Acquisition Cost
        return round(cap_rate(net_operating_income=self.calculate_annual_noi(),
                              purchase_price=self.real_estate_property.purchase_price), 2)

    def calculate_annual_gross_yield(self):
        # Annual Rental Income / Property Purchase Price
        return round(gross_yield(annual_rent_income=self.calculate_annual_rent_income(),
                                 purchase_price=self.real_estate_property.purchase_price), 2)

    def calculate_net_profit(self) -> int:
        # Total Revenue - Total Expenses
        return self.calculate_total_revenue() - self.calculate_total_expenses()

    def estimate_property_value_with_noi(self):
        return self.calculate_annual_noi() / (self.calculate_annual_cap_rate() / 100)

    # Purchase
    @abstractmethod
    def calculate_broker_purchase_cost(self):
        pass

    @abstractmethod
    def calculate_closing_costs(self) -> int:
        pass

    def calculate_price_per_meter(self, weight_for_balcony_meter: float = 0.5) -> int:
        house_meters = self.real_estate_property.square_meters + weight_for_balcony_meter * self.real_estate_property.balcony_square_meter
        return round(self.real_estate_property.purchase_price / house_meters)

    def calculate_total_renovation_expenses(self):
        if isinstance(self.renovation_expenses, dict):
            return sum(list(self.renovation_expenses.values()))
        return self.renovation_expenses

    def calculate_purchase_additional_transactions_cost(self):
        if isinstance(self.additional_transaction_costs_dic, dict):
            return sum(list(self.additional_transaction_costs_dic.values()))
        return self.additional_transaction_costs_dic

    def calculate_total_equity_needed_for_purchase(self) -> int:
        return round((self.equity_required_by_percentage / 100) * self.real_estate_property.purchase_price) + \
               self.calculate_closing_costs()

    def calculate_equity_payments(self) -> List[int]:
        equity_for_house_purchase = round(
            (self.equity_required_by_percentage / 100) * self.real_estate_property.purchase_price)

        return [self.calculate_closing_costs() + equity_for_house_purchase]

    # Taxes

    @abstractmethod
    def calculate_purchase_tax(self) -> int:
        pass

    @abstractmethod
    def calculate_monthly_rental_property_taxes(self) -> int:
        pass

    def calculate_annual_rental_property_taxes(self) -> int:
        return 12 * self.calculate_monthly_rental_property_taxes()

    @abstractmethod
    def calculate_capital_gain_tax(self) -> int:
        pass


    # Holding Expenses

    def calculate_monthly_property_management_fees(self, management_fees_percentage: Optional[float] = None):
        if management_fees_percentage is None:
            management_fees_percentage = self.management_fees_percentage
        return management_fees_percentage * self.real_estate_property.monthly_rent_income

    def calculate_annual_property_management_fees(self, management_fees_percentage: Optional[float] = None) -> int:
        return 12 * self.calculate_monthly_property_management_fees(management_fees_percentage)

    def calculate_monthly_insurances_expenses(self) -> int:
        return round(self.calculate_annual_insurances_expenses() / 12)

    @abstractmethod
    def calculate_annual_insurances_expenses(self) -> int:
        pass

    def calculate_monthly_maintenance_and_repairs(self) -> int:
        return round(self.annual_maintenance_cost_percentage * self.real_estate_property.monthly_rent_income)

    def calculate_annual_maintenance_and_repairs(self) -> int:
        return 12 * self.calculate_monthly_maintenance_and_repairs()

    def calculate_monthly_vacancy_cost(self, vacancy_percentage: Optional[float] = None):
        if vacancy_percentage is None:
            vacancy_percentage = self.vacancy_percentage
        return round(vacancy_percentage * self.real_estate_property.monthly_rent_income)

    def calculate_annual_vacancy_cost(self,  vacancy_percentage: Optional[float] = None):
        return 12 * self.calculate_monthly_vacancy_cost(vacancy_percentage)

    @abstractmethod
    def calculate_monthly_operating_expenses(self) -> int:
        pass

    def calculate_annual_operating_expenses(self) -> int:
        return 12 * self.calculate_monthly_operating_expenses()

    # Holding Revenues

    def calculate_annual_rent_income(self) -> int:
        return 12 * self.real_estate_property.monthly_rent_income

    # Selling
    def calculate_annual_estimated_property_value(self, years: Optional[int] = None, annual_appreciation_percentage: Optional[int] = None):
        if years is None:
            years = self.years_to_exit
        if annual_appreciation_percentage is None:
            annual_appreciation_percentage = self.real_estate_property.annual_appreciation_percentage
        return [self.calculate_estimated_property_value(annual_appreciation_percentage, i) for i in range(years + 1)]

    def calculate_estimated_property_value(self, years: Optional[int] = None, annual_appreciation_percentage: Optional[int] = None):
        if years is None:
            years = self.years_to_exit
        if annual_appreciation_percentage is None:
            annual_appreciation_percentage = self.real_estate_property.annual_appreciation_percentage
        return self.real_estate_property.after_repair_value * np.power((1 + annual_appreciation_percentage / 100), years)

    def estimate_sale_price(self, annual_appreciation_percentage: Optional[int] = None) -> int:
        if annual_appreciation_percentage is None:
            annual_appreciation_percentage = self.real_estate_property.annual_appreciation_percentage
        return round(self.calculate_estimated_property_value(annual_appreciation_percentage=annual_appreciation_percentage))

    @abstractmethod
    def calculate_selling_expenses(self) -> int:
        pass

    def calculate_sale_proceeds(self) -> int:
        return self.estimate_sale_price() - self.calculate_selling_expenses()

    def calculate_mortgage_remain_balance_in_exit(self) -> int:
        mortgage_done = self.mortgage.get_num_of_payments() <= (self.years_to_exit * 12)
        return 0 if mortgage_done else round(self.mortgage.get_annual_remain_balances()[self.years_to_exit])

    # General

    def calculate_total_revenue(self) -> int:
        return self.estimate_sale_price() + self.years_to_exit * self.calculate_annual_rent_income()

    @abstractmethod
    def calculate_total_expenses(self) -> int:
        pass

    def calculate_annual_revenue_distribution(self) -> List[int]:
        return [self.calculate_annual_rent_income() for _ in range(self.years_to_exit)] + [self.estimate_sale_price()]

    @abstractmethod
    def calculate_annual_expenses_distribution(self) -> List[float]:
        pass

    def get_annual_property_remain_balances(self):
        return [round(balance) for balance in self.mortgage.get_annual_remain_balances()]

    # Plotting Methods

    def plot_irr_vs_initial_equity_percentage(self):
        x_s = np.linspace(25, 100, (100 - 25) // 5 + 1)
        y_s = []
        for x in x_s:
            self.equity_required_by_percentage = x
            self.mortgage.tracks[0].initial_loan_amount = self.real_estate_property.purchase_price * (1 - x / 100)
            y_s.append(self.calculate_annual_irr())

        plt.plot(x_s, y_s)
        plt.xlabel('Equity Percentage')
        plt.ylabel('Yearly IRR')
        plt.title('Yearly IRR vs Equity Percentage')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'{x},{y:.2f}', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_irr_vs_years_to_exit(self):
        x_s = [i for i in range(1, 31)]
        y_s = []
        for x in x_s:
            self.years_to_exit = x
            y_s.append(self.calculate_annual_irr())

        plt.plot(x_s, y_s)
        plt.xlabel('Years to Exit')
        plt.ylabel('Annual IRR')
        plt.title('Annual IRR vs Years to Exit')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x}, {y:.2f}%)', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_cash_flow_vs_initial_equity_percentage(self):
        x_s = np.linspace(25, 100, (100 - 25) // 5 + 1)
        y_s = []
        for x in x_s:
            self.equity_required_by_percentage = x
            self.mortgage.tracks[0].initial_loan_amount = self.real_estate_property.purchase_price * (1 - x / 100)
            y_s.append(self.calculate_net_annual_cash_flow())

        plt.plot(x_s, y_s)
        plt.xlabel('Equity Percentage')
        plt.ylabel('Yearly Cash Flow')
        plt.title('Yearly Cash Flow vs Equity Percentage')

        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x}, {y:.2f})', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_investment_cash_flow(self):
        x_s = [i for i in range(1, self.years_to_exit + 2)]
        y_s = self.calculate_annual_cash_flow_distribution()

        plt.plot(x_s, y_s)
        plt.xlabel('Years')
        plt.ylabel('Annual Cash Flow')
        plt.title('Annual Cash Flow vs Years of investment')

        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x}, {y:.2f})', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_estimated_property_value(self, year_to_exit: Optional[int] = None, annual_appreciation_percentage: Optional[int] = None):
        if year_to_exit is None:
            year_to_exit = self.years_to_exit
        if annual_appreciation_percentage is None:
            annual_appreciation_percentage = self.real_estate_property.annual_appreciation_percentage
        x_s = [i for i in range(1, year_to_exit + 2)]
        y_s = self.calculate_annual_estimated_property_value(year_to_exit, annual_appreciation_percentage)
        y_s = [round(y / 1_000_000, 2) for y in y_s]

        plt.plot(x_s, y_s)
        plt.xlabel('Years')
        plt.ylabel('Estimated Property Value')
        plt.title('Estimated Property Value vs Years of investment')

        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x}, {y:.2f}M)', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_property_equity_vs_years(self, year_to_exit: Optional[int] = None, annual_appreciation_percentage: Optional[int] = None):
        if year_to_exit is None:
            year_to_exit = self.years_to_exit
        if annual_appreciation_percentage is None:
            annual_appreciation_percentage = self.real_estate_property.annual_appreciation_percentage
        x_s = [i for i in range(1, year_to_exit + 2)]
        annual_estimated_property_value = self.calculate_annual_estimated_property_value(year_to_exit,
                                                                                         annual_appreciation_percentage)
        print(annual_estimated_property_value)
        loan_remain_balance = self.get_annual_property_remain_balances()
        print(loan_remain_balance)
        property_equity = [a - b for a, b in zip(annual_estimated_property_value, loan_remain_balance)]
        property_equity_in_years = [round(equity / 1_000_000, 2) for equity in property_equity[:year_to_exit + 1]]
        plt.plot(x_s, property_equity_in_years)
        plt.xlabel('Years')
        plt.ylabel('Property Equity')
        plt.title('Property Equity vs Years')

        for x, y in zip(x_s, property_equity_in_years):
            plt.text(x, y, f'({x}, {y:.2f}M)', ha='left', va='bottom')

        plt.legend()
        plt.show()


    def plot_net_profit_vs_year_to_exit(self):
        x_s = [i for i in range(3, 31)]
        y_s = []
        for x in x_s:
            self.years_to_exit = x
            y_s.append(self.calculate_net_profit())

        plt.plot(x_s, y_s)
        plt.xlabel('Years to Exit')
        plt.ylabel('Net Profit')
        plt.title('Net Profit vs Years to Exit')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x}, {y / 1000000:.2f}M)', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_annual_irr_vs_purchase_price(self):
        x_s = [self.real_estate_property.purchase_price + step * 50_000 for step in range(-4, 5)]
        y_s = []
        for x in x_s:
            self.real_estate_property.purchase_price = x
            self.real_estate_property.after_repair_value = x
            self.mortgage.tracks[0].initial_loan_amount = self.real_estate_property.purchase_price * (
                    1 - self.equity_required_by_percentage / 100)
            y_s.append(self.calculate_annual_irr())

        plt.plot(x_s, y_s)
        plt.xlabel('Purchase Price')
        plt.ylabel('Yearly IRR')
        plt.title('Yearly IRR vs Purchase Price')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x / 1_000_000:.2f}M, {y :.2f}%)', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_annual_cap_rate_vs_purchase_price(self):
        x_s = [self.real_estate_property.purchase_price + step * 50_000 for step in range(-4, 5)]
        y_s = []
        for x in x_s:
            self.real_estate_property.purchase_price = x
            self.real_estate_property.after_repair_value = x
            self.mortgage.tracks[0].initial_loan_amount = self.real_estate_property.purchase_price * (
                    1 - self.equity_required_by_percentage / 100)
            y_s.append(self.calculate_annual_cap_rate())

        plt.plot(x_s, y_s)
        plt.xlabel('Purchase Price')
        plt.ylabel('Annual Cap Rate')
        plt.title('Annual Cap Rate vs Purchase Price')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x / 1_000_000:.2f}M, {y :.2f}%)', ha='left', va='bottom')

        plt.legend()
        plt.show()


    def plot_annual_irr_vs_annual_appreciation_percentage(self):
        x_s = list(np.arange(0, 7, 0.5))
        y_s = []
        for x in x_s:
            self.real_estate_property.annual_appreciation_percentage = x
            y_s.append(self.calculate_annual_irr())

        plt.plot(x_s, y_s)
        plt.xlabel('Annual Appreciation Percentage')
        plt.ylabel('Yearly IRR')
        plt.title('Yearly IRR vs Annual Appreciation Percentage')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x:.2f}%, {y :.2f}%)', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_annual_irr_vs_rent_price(self):
        x_s = [self.real_estate_property.monthly_rent_income + step * 200 for step in range(-4, 5)]
        y_s = []
        for x in x_s:
            self.real_estate_property.monthly_rent_income = x
            y_s.append(self.calculate_annual_irr())

        plt.plot(x_s, y_s)
        plt.xlabel('Rent Price')
        plt.ylabel('Annual IRR')
        plt.title('Annual IRR vs Rent Price')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x:.2f}$, {y :.2f}%)', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_annual_cash_flow_vs_rent_price(self):
        x_s = [self.real_estate_property.monthly_rent_income + step * 200 for step in range(-4, 5)]
        y_s = []
        for x in x_s:
            self.real_estate_property.monthly_rent_income = x
            y_s.append(self.calculate_net_annual_cash_flow())

        plt.plot(x_s, y_s)
        plt.xlabel('Rent Price')
        plt.ylabel('Annual Cash Flow')
        plt.title('Annual Cash Flow vs Rent Price')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x:.2f}$, {y}$)', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def plot_annual_irr_vs_mortgage_interest_only_period(self):
        x_s = [year * 12 for year in range(12)]
        y_s = []
        for x in x_s:
            for track in self.mortgage.tracks:
                track.interest_only_period = x
            y_s.append(self.calculate_annual_irr())

        plt.plot(x_s, y_s)
        plt.xlabel('mortgage_interest_only_period')
        plt.ylabel('Annual IRR')
        plt.title('Annual IRR vs mortgage_interest_only_period')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x}, {y :.2f}%)', ha='left', va='bottom')

        plt.legend()
        plt.show()


if __name__ == "__main__":
    investor = RealEstateInvestor(25_000, 0, RealEstateInvestmentType.SingleApartment, 1_000_000, 0)
    investors_portfolio = RealEstateInvestorsPortfolio(investor)
    property = RealEstateProperty(purchase_price=1_850_000,
                                  monthly_rent_income=4100,
                                  square_meters=60,
                                  parking_spots=1,
                                  warehouse=False,
                                  balcony_square_meter=13,
                                  after_repair_value=1_850_000,
                                  annual_appreciation_percentage=3.5)

    mortgage = MortgagePipeline(ConstantNotLinked(interest_rate=3.5 / 100,
                                                  num_payments=360,
                                                  initial_loan_amount=0.6 * property.purchase_price,
                                                  interest_only_period=0 * 12))

    model = SingleHouseModel(investors_portfolio=investors_portfolio,
                             mortgage=mortgage,
                             real_estate_property=property,
                             years_to_exit=30,
                             average_interest_in_exit={mortgage.tracks[0].__class__: mortgage.tracks[0].interest_rate},
                             mortgage_advisor_cost=6000,
                             appraiser_cost=2000,
                             lawyer_cost=5600,
                             escort_costs=0,
                             additional_transaction_costs_dic={"total": 1340},
                             renovation_expenses_dic=None,
                             furniture_cost=40_000,
                             broker_purchase_percentage=0.0,
                             broker_rent_percentage=0.0,
                             broker_sell_percentage=0.0,
                             vacancy_percentage=4 / 100,
                             annual_maintenance_cost_percentage=4 / 100,
                             annual_life_insurance_cost=400,
                             annual_house_insurance_cost=300,
                             construction_input_index_annual_growth=2,
                             equity_required_by_percentage=40,
                             years_until_key_reception=2,
                             contractor_payment_distribution=[0.5, 0, 0.5],
                             management_fees_percentage=0
                             )

    print(model.estimate_property_value_with_noi())
    # print(model.calculate_annual_cash_flow_distribution())
    # print(model.calculate_net_profit())
    print(model.annual_irr_vs_mortgage_interest_only_period())
    # model.plot_property_equity_vs_years()
    # print(round(model.calculate_net_profit() / 1000000, 2))
    # print(model.calculate_annual_noi() / (model.calculate_annual_cap_rate() / 100))
    # model.plot_cash_flow_vs_equity_percentage()
    # model.plot_irr_vs_equity_percentage()
    # 27820
    # print(f"Price per meter: {model.calculate_price_per_meter()}")
    # print(f"Loan to cost: {model.calculate_loan_to_cost()}")
    # print(f"Loan to value :{model.calculate_loan_to_value()}")
    # print(f"Renovation expenses {model.calculate_total_renovation_expenses()}")
    # print(f"calculate_purchase_additional_transactions_cost: {model.calculate_purchase_additional_transactions_cost()}")
    # print(f"calculate_purchase_tax {model.calculate_purchase_tax()}")
    # print(f"calculate_closing_costs {model.calculate_closing_costs()}")
    # print(f"calculate_broker_purchase_cost {model.calculate_broker_purchase_cost()}")
    # print(f"calculate_monthly_operating_expenses {model.calculate_monthly_operating_expenses()}")
    # print(f"Cash on cash {model.calculate_cash_on_cash()}")
    # print(f"Net Yearly Cash Flow {model.calculate_net_yearly_cash_flow()}")
    # print(f"Net Monthly Cash Flow {model.calculate_net_monthly_cash_flow()}")
    # print(f"Yearly IRR: {model.calculate_yearly_irr()}")
    # print(f"calculate_annual_rent_income {model.calculate_annual_rent_income()}")
    # print(f"ROI: {model.calculate_roi()}")
    # print(f"calculate_monthly_noi: {model.calculate_monthly_noi()}")
    # print(f"calculate_annual_noi: {model.calculate_annual_noi()}")
    # print(f"calculate_monthly_rental_property_taxes: {model.calculate_monthly_rental_property_taxes()}")
    # print(f"calculate_annual_rental_property_taxes: {model.calculate_annual_rental_property_taxes()}")
    # print(f"calculate_cap_rate: {model.calculate_cap_rate()}")
    # print(f"calculate_gross_yield: {model.calculate_gross_yield()}")
    # print(f"calculate_dscr: {model.calculate_dscr()}")
    # print(f"calculate_monthly_insurances_expenses: {model.calculate_monthly_insurances_expenses()}")
    # print(f"calculate_annual_insurances_expenses: {model.calculate_annual_insurances_expenses()}")
    # print(f"calculate_monthly_maintenance_and_repairs: {model.calculate_monthly_maintenance_and_repairs()}")
    # print(f"calculate_annual_maintenance_and_repairs: {model.calculate_annual_maintenance_and_repairs()}")
    # print(f"calculate_monthly_vacancy_cost: {model.calculate_monthly_vacancy_cost()}")
    # print(f"calculate_annual_vacancy_cost: {model.calculate_annual_vacancy_cost()}")
    # print(f"estimate_sale_price: {model.estimate_sale_price()}")
    # print(f"calculate_selling_expenses: {model.calculate_selling_expenses()}")
    # print(f"calculate_sale_proceeds: {model.calculate_sale_proceeds()}")
    # print(f"calculate_annual_revenue: {model.calculate_annual_revenue()}")
    # print(f"calculate_total_revenue: {model.calculate_total_revenue()}")
    # print(f"calculate_annual_revenue_distribution: {model.calculate_annual_revenue_distribution()}")
    # print(f"calculate_annual_operating_expenses: {model.calculate_annual_operating_expenses()}")
    # print(f"calculate_annual_cash_flow: {model.calculate_annual_cash_flow()}")
    # print(f"calculate_mortgage_remain_balance_in_exit: {model.calculate_mortgage_remain_balance_in_exit()}")
    # print(f"calculate_constructor_index_linked_compensation: {model.calculate_constructor_index_linked_compensation()}")
    # print(f"calculate_total_expenses: {model.calculate_total_expenses()}")
    # print(f"calculate_equity_needed_for_purchase: {model.calculate_total_equity_needed_for_purchase()}")
    # print(f"calculate_contractor_payments: {model.calculate_equity_payments()}")
    # print(f"calculate_annual_expenses_distribution: {model.calculate_annual_expenses_distribution()}")
    # print(f"calculate_monthly_property_management_fees: {model.calculate_monthly_property_management_fees()}")
    # print(f"calculate_annual_property_management_fees: {model.calculate_annual_property_management_fees()}")
    # print(f"calculate_dti: {model.calculate_dti()}")
    # print(f"calculate_net_profit: {model.calculate_net_profit()}")
    # print(f"calculate_capital_gain_tax: {model.calculate_capital_gain_tax()}")




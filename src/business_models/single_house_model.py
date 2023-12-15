from typing import Dict, Optional, List, Union

import matplotlib.pyplot as plt
import matplotlib
from src.investors.real_estate_investors_portfolio import RealEstateInvestorsPortfolio
from src.mortgage.mortgage_pipeline import MortgagePipeline
import numpy as np
import numpy_financial as npf
from src.business_models.real_estate_property import RealEstateProperty
from src.mortgage.mortgage_tracks.mortgage_track import MortgageTrack
from src.business_models.real_estate_financial_utils import gross_yield, \
    loan_to_cost, loan_to_value, cash_of_cash, return_on_investment, noi, \
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
                 equity_required_by_percentage: float = 0.25,
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
        self.equity_required_by_percentage = equity_required_by_percentage
        self.furniture_cost = furniture_cost
        self.additional_transaction_costs_dic = additional_transaction_costs_dic
        self.renovation_expenses = renovation_expenses_dic
        self.management_fees_percentage = management_fees_percentage

    def validate_parameters(self):
        # TODO
        pass

    # Financial Metrics and Calculations

    def calculate_loan_to_cost(self) -> float:
        """
        Calculate the Loan-to-Cost ratio.

        :return: The Loan-to-Cost ratio.
        """
        return round(loan_to_cost(loan_amount=self.mortgage.total_initial_loan_amount,
                                  total_project_cost=self.real_estate_property.purchase_price), 2)

    def calculate_loan_to_value(self) -> float:
        """
        Calculate the Loan-to-Value ratio.

        :return: The Loan-to-Value ratio.
        """
        return loan_to_value(loan_amount=self.mortgage.total_initial_loan_amount,
                             after_repair_value=self.real_estate_property.after_repair_value)

    def calculate_net_monthly_cash_flow(self) -> int:
        """
        Calculate the net monthly cash flow.

        :return: The net monthly cash flow.
        """
        # This method assumes the interest is constant
        monthly_revenues = self.real_estate_property.monthly_rent_income
        print(f"Monthly revenues: {monthly_revenues}")
        monthly_expenses = self.calculate_monthly_operating_expenses() + self.mortgage.calculate_initial_monthly_payment()
        print(f"monthly_expenses: {monthly_expenses}")
        return monthly_revenues - monthly_expenses

    def calculate_net_annual_cash_flow(self) -> int:
        """
        Calculate the net annual cash flow.

        :return: The net annual cash flow.
        """
        return 12 * self.calculate_net_monthly_cash_flow()

    def calculate_cash_on_cash(self) -> float:
        """
        Calculate the Cash-on-Cash return.

        :return: The Cash-on-Cash return.
        """
        return cash_of_cash(net_annual_cash_flow=self.calculate_net_annual_cash_flow(),
                            total_equity_needed_for_purchase=self.calculate_total_equity_needed_for_purchase())

    def calculate_annual_irr(self) -> float:
        """
        Calculate the annual Internal Rate of Return (IRR).

        :return: The annual IRR.
        """
        annual_cash_flow_distribution = self.calculate_annual_cash_flow_distribution()
        return round(100 * npf.irr(annual_cash_flow_distribution), 2)

    def calculate_annual_cash_flow_distribution(self) -> List[int]:
        """
        Calculate the annual cash flow distribution.

        :return: The list of annual cash flow distribution.
        """
        annual_revenue_distribution = self.calculate_annual_revenue_distribution()
        annual_expenses_distribution = self.calculate_annual_expenses_distribution()
        annual_cash_flow_distribution = [round(a - b) for a, b in
                                         zip(annual_revenue_distribution, annual_expenses_distribution)]
        return annual_cash_flow_distribution

    def calculate_roi(self) -> float:
        """
        Calculate the Return on Investment (ROI).

        :return: The ROI.
        """
        # Return on investment
        # Net Profit / Cost Of Investment
        return return_on_investment(net_profit=self.calculate_net_profit(),
                                    total_equity_needed_for_purchase=self.calculate_total_equity_needed_for_purchase())

    def calculate_monthly_noi(self) -> int:
        """
        Calculate the monthly Net Operating Income (NOI).

        :return: The monthly NOI.
        """
        # Net Operating Income
        # (Operating Income - Operating Expenses)
        return noi(operating_income=self.real_estate_property.monthly_rent_income,
                   operating_expenses=self.calculate_monthly_operating_expenses())

    def calculate_annual_noi(self) -> int:
        """
        Calculate the annual Net Operating Income (NOI).

        :return: The annual NOI.
        """
        return 12 * self.calculate_monthly_noi()

    def calculate_annual_cap_rate(self) -> float:
        """
        Calculate the annual Capitalization Rate (Cap Rate).

        :return: The annual Cap Rate.
        """
        # NOI / Current Market Value or Acquisition Cost
        return round(cap_rate(net_operating_income=self.calculate_annual_noi(),
                              purchase_price=self.real_estate_property.purchase_price), 2)

    def calculate_annual_gross_yield(self) -> float:
        """
        Calculate the annual Gross Yield.

        :return: The annual Gross Yield.
        """
        # Annual Rental Income / Property Purchase Price
        return round(gross_yield(annual_rent_income=self.calculate_annual_rent_income(),
                                 purchase_price=self.real_estate_property.purchase_price), 2)

    def calculate_net_profit(self) -> int:
        """
        Calculate the net profit.

        :return: The net profit.
        """
        # Total Revenue - Total Expenses
        return self.calculate_total_revenue() - self.calculate_total_expenses()

    def estimate_property_value_with_noi(self) -> int:
        """
        Estimate the property value using the Net Operating Income (NOI) and Cap Rate.

        :return: The estimated property value.
        """
        return round(self.calculate_annual_noi() / (self.calculate_annual_cap_rate() / 100))

    # Purchase
    @abstractmethod
    def calculate_broker_purchase_cost(self) -> int:
        """
        Abstract method to calculate the broker purchase cost.
        Implement this method in the concrete subclass.
        """
        pass

    @abstractmethod
    def calculate_closing_costs(self) -> int:
        """
        Abstract method to calculate the closing costs.
        Implement this method in the concrete subclass.

        :return: The calculated closing costs.
        """
        pass

    def calculate_price_per_meter(self, weight_for_balcony_meter: float = 0.5) -> int:
        """
        Calculate the price per meter of the property.

        :param weight_for_balcony_meter: Weight assigned to the balcony square meter.
        :return: The calculated price per meter.
        """
        house_meters = self.real_estate_property.square_meters + weight_for_balcony_meter * self.real_estate_property.balcony_square_meter
        return round(self.real_estate_property.purchase_price / house_meters)

    def calculate_total_renovation_expenses(self) -> int:
        """
        Calculate the total renovation expenses.

        :return: The total renovation expenses.
        """
        if isinstance(self.renovation_expenses, dict):
            return sum(list(self.renovation_expenses.values()))
        return self.renovation_expenses

    def calculate_purchase_additional_transactions_cost(self) -> int:
        """
        Calculate the total additional transaction costs for the purchase.

        :return: The total additional transaction costs.
        """
        if isinstance(self.additional_transaction_costs_dic, dict):
            return sum(list(self.additional_transaction_costs_dic.values()))
        return self.additional_transaction_costs_dic

    def calculate_total_equity_needed_for_purchase(self) -> int:
        """
        Calculate the total equity needed for the property purchase.

        :return: The total equity needed for the purchase.
        """
        return round((self.equity_required_by_percentage / 100) * self.real_estate_property.purchase_price) + \
               self.calculate_closing_costs()

    def calculate_equity_payments(self) -> List[int]:
        """
        Calculate the equity payments.

        :return: A list of calculated equity payments.
        """
        equity_for_house_purchase = round(
            (self.equity_required_by_percentage / 100) * self.real_estate_property.purchase_price)

        return [self.calculate_closing_costs() + equity_for_house_purchase]

    # Taxes

    @abstractmethod
    def calculate_purchase_tax(self) -> int:
        """
        Abstract method to calculate the purchase tax.
        Implement this method in the concrete subclass.

        :return: The calculated purchase tax.
        """
        pass

    @abstractmethod
    def calculate_monthly_rental_property_taxes(self) -> int:
        """
        Abstract method to calculate the monthly rental property taxes.
        Implement this method in the concrete subclass.

        :return: The calculated monthly rental property taxes.
        """
        pass

    def calculate_annual_rental_property_taxes(self) -> int:
        """
        Calculate the annual rental property taxes.

        :return: The calculated annual rental property taxes.
        """
        return 12 * self.calculate_monthly_rental_property_taxes()

    @abstractmethod
    def calculate_capital_gain_tax(self) -> int:
        """
        Abstract method to calculate the capital gain tax.
        Implement this method in the concrete subclass.

        :return: The calculated capital gain tax.
        """
        pass


    # Holding Expenses

    def calculate_monthly_property_management_fees(self, management_fees_percentage: Optional[float] = None) -> int:
        """
        Calculate the monthly property management fees.

        :param management_fees_percentage: Optional. Custom management fees percentage. If not provided, uses the default value.
        :return: The calculated monthly property management fees.
        """
        if management_fees_percentage is None:
            management_fees_percentage = self.management_fees_percentage
        return round(management_fees_percentage * self.real_estate_property.monthly_rent_income)

    def calculate_annual_property_management_fees(self, management_fees_percentage: Optional[float] = None) -> int:
        """
        Calculate the annual property management fees.

        :param management_fees_percentage: Optional. Custom management fees percentage. If not provided, uses the default value.
        :return: The calculated annual property management fees.
        """
        return 12 * self.calculate_monthly_property_management_fees(management_fees_percentage)

    def calculate_monthly_insurances_expenses(self) -> int:
        """
        Calculate the monthly insurance expenses.

        :return: The calculated monthly insurance expenses.
        """
        return round(self.calculate_annual_insurances_expenses() / 12)

    @abstractmethod
    def calculate_annual_insurances_expenses(self) -> int:
        """
        Abstract method to calculate the annual insurance expenses.
        Implement this method in the concrete subclass.

        :return: The calculated annual insurance expenses.
        """
        pass

    def calculate_monthly_maintenance_and_repairs(self) -> int:
        """
        Calculate the monthly maintenance and repairs expenses.

        :return: The calculated monthly maintenance and repairs expenses.
        """
        return round(self.annual_maintenance_cost_percentage * self.real_estate_property.monthly_rent_income)

    def calculate_annual_maintenance_and_repairs(self) -> int:
        """
        Calculate the annual maintenance and repairs expenses.

        :return: The calculated annual maintenance and repairs expenses.
        """
        return 12 * self.calculate_monthly_maintenance_and_repairs()

    def calculate_monthly_vacancy_cost(self, vacancy_percentage: Optional[float] = None) -> int:
        """
        Calculate the monthly vacancy cost.

        :param vacancy_percentage: Optional. Custom vacancy percentage. If not provided, uses the default value.
        :return: The calculated monthly vacancy cost.
        """
        if vacancy_percentage is None:
            vacancy_percentage = self.vacancy_percentage
        return round(vacancy_percentage * self.real_estate_property.monthly_rent_income)

    def calculate_annual_vacancy_cost(self, vacancy_percentage: Optional[float] = None) -> int:
        """
        Calculate the annual vacancy cost.

        :param vacancy_percentage: Optional. Custom vacancy percentage. If not provided, uses the default value.
        :return: The calculated annual vacancy cost.
        """
        return 12 * self.calculate_monthly_vacancy_cost(vacancy_percentage)

    @abstractmethod
    def calculate_monthly_operating_expenses(self) -> int:
        """
        Abstract method to calculate the monthly operating expenses.
        Implement this method in the concrete subclass.

        :return: The calculated monthly operating expenses.
        """
        pass

    def calculate_annual_operating_expenses(self) -> int:
        """
        Calculate the annual operating expenses.

        :return: The calculated annual operating expenses.
        """
        return 12 * self.calculate_monthly_operating_expenses()

    # Holding Revenues

    def calculate_annual_rent_income(self) -> int:
        return 12 * self.real_estate_property.monthly_rent_income

    # Selling
    def calculate_annual_estimated_property_value(self, years: Optional[int] = None, annual_appreciation_percentage: Optional[int] = None) -> List[int]:
        """
        Calculate the annual estimated property value over a specified number of years.

        :param years: Optional. Number of years for estimation. If not provided, uses the default value.
        :param annual_appreciation_percentage: Optional. Custom annual appreciation percentage. If not provided, uses the default value.
        :return: A list of annual estimated property values.
        """
        if years is None:
            years = self.years_to_exit
        if annual_appreciation_percentage is None:
            annual_appreciation_percentage = self.real_estate_property.annual_appreciation_percentage
        return [self.calculate_estimated_property_value(annual_appreciation_percentage, i) for i in range(years + 1)]

    def calculate_estimated_property_value(self, years: Optional[int] = None, annual_appreciation_percentage: Optional[int] = None) -> int:
        """
        Calculate the estimated property value after a specified number of years.

        :param years: Optional. Number of years for estimation. If not provided, uses the default value.
        :param annual_appreciation_percentage: Optional. Custom annual appreciation percentage. If not provided, uses the default value.
        :return: The estimated property value after the specified number of years.
        """
        if years is None:
            years = self.years_to_exit
        if annual_appreciation_percentage is None:
            annual_appreciation_percentage = self.real_estate_property.annual_appreciation_percentage
        return round(self.real_estate_property.after_repair_value * np.power((1 + annual_appreciation_percentage / 100), years))

    def estimate_sale_price(self, annual_appreciation_percentage: Optional[int] = None) -> int:
        """
        Estimate the sale price of the property.

        :param annual_appreciation_percentage: Optional. Custom annual appreciation percentage. If not provided, uses the default value.
        :return: The estimated sale price of the property.
        """
        if annual_appreciation_percentage is None:
            annual_appreciation_percentage = self.real_estate_property.annual_appreciation_percentage
        return round(self.calculate_estimated_property_value(annual_appreciation_percentage=annual_appreciation_percentage))

    @abstractmethod
    def calculate_selling_expenses(self) -> int:
        """
        Abstract method to calculate the selling expenses.
        Implement this method in the concrete subclass.

        :return: The calculated selling expenses.
        """
        pass

    def calculate_sale_proceeds(self) -> int:
        """
        Calculate the net sale proceeds.

        :return: The calculated net sale proceeds.
        """
        return self.estimate_sale_price() - self.calculate_selling_expenses()

    def calculate_mortgage_remain_balance_in_exit(self) -> int:
        """
        Calculate the remaining mortgage balance at the exit.

        :return: The remaining mortgage balance at the exit.
        """
        mortgage_done = self.mortgage.get_num_of_payments() <= (self.years_to_exit * 12)
        return 0 if mortgage_done else round(self.mortgage.get_annual_remain_balances()[self.years_to_exit])

    # General

    def calculate_total_revenue(self) -> int:
        """
        Calculate the total revenue over the investment period.

        :return: The calculated total revenue.
        """
        return self.estimate_sale_price() + self.years_to_exit * self.calculate_annual_rent_income()

    @abstractmethod
    def calculate_total_expenses(self) -> int:
        """
        Abstract method to calculate the total expenses.
        Implement this method in the concrete subclass.

        :return: The calculated total expenses.
        """
        pass

    def calculate_annual_revenue_distribution(self) -> List[int]:
        """
        Calculate the annual revenue distribution over the investment period.

        :return: A list of annual revenue distribution.
        """
        return [self.calculate_annual_rent_income() for _ in range(self.years_to_exit)] + [
            self.estimate_sale_price()]

    @abstractmethod
    def calculate_annual_expenses_distribution(self) -> List[float]:
        """
        Abstract method to calculate the annual expenses distribution.
        Implement this method in the concrete subclass.

        :return: A list of annual expenses distribution.
        """
        pass

    def get_annual_property_remain_balances(self) -> List[int]:
        """
        Get the annual property remaining balances.

        :return: A list of annual property remaining balances.
        """
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


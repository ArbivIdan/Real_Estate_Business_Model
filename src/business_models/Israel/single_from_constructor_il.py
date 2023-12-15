from typing import Optional, List, Dict, Union
import matplotlib.pyplot as plt
import numpy as np

from src.investors.Israel.real_estate_investment_type import RealEstateInvestmentType
from src.investors.real_estate_investor import RealEstateInvestor
from src.investors.real_estate_investors_portfolio import RealEstateInvestorsPortfolio
from src.mortgage.mortgage_pipeline import MortgagePipeline
from src.mortgage.mortgage_tracks.constant_not_linked import ConstantNotLinked
from src.mortgage.mortgage_tracks.mortgage_track import MortgageTrack
from src.business_models.real_estate_property import RealEstateProperty
from src.business_models.Israel.single_house_israel_model import SingleHouseIsraelModel


class SingleFromConstructorIL(SingleHouseIsraelModel):
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
                 management_fees_percentage: int = 0,
                 years_until_key_reception: int = 0,
                 contractor_payment_distribution: List[float] = 0,
                 construction_input_index_annual_growth: int = 0
                ):

        super().__init__(
            investors_portfolio, mortgage, real_estate_property,
            years_to_exit=years_to_exit,
            average_interest_in_exit=average_interest_in_exit,
            mortgage_advisor_cost=mortgage_advisor_cost,
            appraiser_cost=appraiser_cost,
            lawyer_cost=lawyer_cost,
            escort_costs=escort_costs,
            additional_transaction_costs_dic=additional_transaction_costs_dic,
            renovation_expenses_dic=renovation_expenses_dic,
            furniture_cost=furniture_cost,
            broker_purchase_percentage=broker_purchase_percentage,
            broker_rent_percentage=broker_rent_percentage,
            broker_sell_percentage=broker_sell_percentage,
            vacancy_percentage=vacancy_percentage,
            annual_maintenance_cost_percentage=annual_maintenance_cost_percentage,
            annual_life_insurance_cost=annual_life_insurance_cost,
            annual_house_insurance_cost=annual_house_insurance_cost,
            equity_required_by_percentage=equity_required_by_percentage,
            management_fees_percentage=management_fees_percentage,
        )

        self.years_until_key_reception = years_until_key_reception
        self.contractor_payment_distribution = contractor_payment_distribution
        self.construction_input_index_annual_growth = construction_input_index_annual_growth

    def calculate_total_equity_needed_for_purchase(self) -> int:
        """
        Calculate the total equity needed for the property purchase.

        :return: The total equity needed for the purchase.
        """
        return super().calculate_total_equity_needed_for_purchase() + self.calculate_constructor_index_linked_compensation()

    def calculate_constructor_index_linked_compensation(self, years_until_key_reception: Optional[int] = None) -> int:
        """
        Calculate the compensation linked to the construction index.

        :param years_until_key_reception: Optional. Number of years until key reception. If not provided, uses the default value.
        :return: The calculated compensation linked to the construction index.
        """
        if self.years_until_key_reception <= 0:
            return 0
        if years_until_key_reception is None:
            years_until_key_reception = self.years_until_key_reception
        remain_balance_for_purchase = self.real_estate_property.purchase_price * (
                1 - ((self.equity_required_by_percentage * self.contractor_payment_distribution[0]) / 100))
        # TODO: covert to consts. 0.4 is the percentage of the remain balance that is linked (by law)
        remain_balance_linked_amount = 0.4 * remain_balance_for_purchase
        return round(remain_balance_linked_amount * (
                np.power((1 + self.construction_input_index_annual_growth / 100), years_until_key_reception) - 1))

    def calculate_equity_payments(self) -> List[int]:
        """
        Calculate the equity payments over the investment period.

        :return: A list of calculated equity payments.
        """
        equity_for_house_purchase = round(
            (self.equity_required_by_percentage / 100) * self.real_estate_property.purchase_price)
        equity_payments = [round(equity_for_house_purchase * self.contractor_payment_distribution[i]) for i in
                           range(self.years_until_key_reception + 1)]
        equity_payments[0] += self.calculate_closing_costs()
        equity_payments[-1] += self.calculate_constructor_index_linked_compensation()

        return equity_payments

    def calculate_mortgage_remain_balance_in_exit(self) -> int:
        """
        Calculate the remaining mortgage balance at the exit.

        :return: The remaining mortgage balance at the exit.
        """
        mortgage_done = self.mortgage.get_num_of_payments() <= (self.years_to_exit * 12)
        return 0 if mortgage_done else round(self.mortgage.get_remain_balances()[(self.years_to_exit - self.years_until_key_reception) * 12])

    def calculate_total_revenue(self) -> int:
        """
        Calculate the total revenue over the investment period.

        :return: The calculated total revenue.
        """
        return self.estimate_sale_price() + (
                self.years_to_exit - self.years_until_key_reception) * self.calculate_annual_rent_income()

    def calculate_total_expenses(self) -> int:
        """
        Calculate the total expenses over the investment period.

        :return: The calculated total expenses.
        """
        return (self.calculate_total_equity_needed_for_purchase() +
                round((
                              self.years_to_exit - self.years_until_key_reception) * self.calculate_annual_operating_expenses()) +
                self.calculate_selling_expenses() +
                self.mortgage.calculate_total_cost_of_borrowing(self.years_to_exit - self.years_until_key_reception,
                                                                self.average_interest_in_exit) +
                self.calculate_capital_gain_tax() +
                self.calculate_mortgage_remain_balance_in_exit())

    def calculate_annual_revenue_distribution(self) -> List[int]:
        """
        Calculate the annual revenue distribution over the investment period.

        :return: A list of annual revenue distribution.
        """
        return [0] * self.years_until_key_reception + \
               [self.calculate_annual_rent_income() for _ in
                range(self.years_to_exit - self.years_until_key_reception)] + \
               [self.estimate_sale_price()]

    def calculate_annual_expenses_distribution(self) -> List[float]:
        """
        Calculate the annual expenses distribution over the investment period.

        :return: A list of annual expenses distribution.
        """
        annual_distribution_operating_expenses = [0 if i < self.years_until_key_reception else self.calculate_annual_operating_expenses() for i in range(self.years_to_exit)] + [0]

        # TODO: I assume here that the mortgage is only taken upon receiving a key, additional scenarios must be created
        estimated_mortgage_monthly_payments = [
                                                  0] * self.years_until_key_reception + self.mortgage.get_annual_payments()[
                                                                                        :(
                                                                                                self.years_to_exit - self.years_until_key_reception)] + [
                                                  0]

        equity_distribution_to_property_purchase = self.calculate_equity_payments() + [0] * (
                self.years_to_exit - self.years_until_key_reception)

        annual_distribution_expenses = [a + b + c for a, b, c in zip(equity_distribution_to_property_purchase,
                                                                     estimated_mortgage_monthly_payments,
                                                                     annual_distribution_operating_expenses)]

        mortgage_early_repayment_fee = self.mortgage.calculate_early_payment_fee(12 * self.years_to_exit,
                                                                                 self.average_interest_in_exit)
        capital_gain_tax = self.calculate_capital_gain_tax()
        selling_expenses = self.calculate_selling_expenses()
        mortgage_remain_balance = self.calculate_mortgage_remain_balance_in_exit()

        annual_distribution_expenses[-1] += (
                selling_expenses + capital_gain_tax + mortgage_early_repayment_fee + mortgage_remain_balance)

        return annual_distribution_expenses

    def get_annual_property_remain_balances(self):
        """
        Get the annual property remaining balances.

        :return: A list of annual property remaining balances.
        """
        return [self.mortgage.get_annual_remain_balances()[0]] * self.years_until_key_reception\
               + [round(balance) for balance in self.mortgage.get_annual_remain_balances()]

    def plot_annual_irr_vs_construction_input_index_annual_growth(self):
        x_s = list(np.arange(0, 5.5, 0.5))
        y_s = []
        for x in x_s:
            self.construction_input_index_annual_growth = x
            y_s.append(self.calculate_annual_irr())

        plt.plot(x_s, y_s)
        plt.xlabel('Construction Input Index Annual Growth')
        plt.ylabel('Yearly IRR')
        plt.title('Yearly IRR vs Construction Input Index Annual Growth')
        for x, y in zip(x_s, y_s):
            plt.text(x, y, f'({x:.2f}%, {y :.2f}%)', ha='left', va='bottom')

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
                                                  initial_loan_amount=round(0.6 * property.purchase_price),
                                                  interest_only_period=0 * 12))

    model = SingleFromConstructorIL(investors_portfolio=investors_portfolio,
                            mortgage=mortgage,
                            real_estate_property=property,
                            years_to_exit=30,
                            average_interest_in_exit={mortgage.tracks[0].__class__: mortgage.tracks[0].interest_rate},
                            mortgage_advisor_cost=6000,
                            appraiser_cost=2000,
                            lawyer_cost=5600,
                            escort_costs=0,
                            additional_transaction_costs_dic=1340,
                            renovation_expenses_dic=0,
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

    investors_portfolio.plot_maximum_property_price_vs_total_available_equity()
    # 27820
    print(f"Price per meter: {model.calculate_price_per_meter()}")
    print(f"Loan to cost: {model.calculate_loan_to_cost()}")
    print(f"Loan to value: {model.calculate_loan_to_value()}")
    print(f"Renovation expenses {model.calculate_total_renovation_expenses()}")
    print(f"calculate_purchase_additional_transactions_cost: {model.calculate_purchase_additional_transactions_cost()}")
    print(f"calculate_purchase_tax {model.calculate_purchase_tax()}")
    print(f"calculate_closing_costs {model.calculate_closing_costs()}")
    print(f"calculate_broker_purchase_cost {model.calculate_broker_purchase_cost()}")
    print(f"calculate_monthly_operating_expenses {model.calculate_monthly_operating_expenses()}")
    print(f"Cash on cash {model.calculate_cash_on_cash()}")
    print(f"Net Yearly Cash Flow {model.calculate_net_annual_cash_flow()}")
    print(f"Net Monthly Cash Flow {model.calculate_net_monthly_cash_flow()}")
    print(f"Yearly IRR: {model.calculate_annual_irr()}")
    print(f"calculate_annual_rent_income {model.calculate_annual_rent_income()}")
    print(f"ROI: {model.calculate_roi()}")
    print(f"calculate_monthly_noi: {model.calculate_monthly_noi()}")
    print(f"calculate_annual_noi: {model.calculate_annual_noi()}")
    print(f"calculate_monthly_rental_property_taxes: {model.calculate_monthly_rental_property_taxes()}")
    print(f"calculate_annual_rental_property_taxes: {model.calculate_annual_rental_property_taxes()}")
    print(f"calculate_cap_rate: {model.calculate_annual_cap_rate()}")
    print(f"calculate_gross_yield: {model.calculate_annual_gross_yield()}")
    print(f"calculate_monthly_insurances_expenses: {model.calculate_monthly_insurances_expenses()}")
    print(f"calculate_annual_insurances_expenses: {model.calculate_annual_insurances_expenses()}")
    print(f"calculate_monthly_maintenance_and_repairs: {model.calculate_monthly_maintenance_and_repairs()}")
    print(f"calculate_annual_maintenance_and_repairs: {model.calculate_annual_maintenance_and_repairs()}")
    print(f"calculate_monthly_vacancy_cost: {model.calculate_monthly_vacancy_cost()}")
    print(f"calculate_annual_vacancy_cost: {model.calculate_annual_vacancy_cost()}")
    print(f"estimate_sale_price: {model.estimate_sale_price()}")
    print(f"calculate_selling_expenses: {model.calculate_selling_expenses()}")
    print(f"calculate_sale_proceeds: {model.calculate_sale_proceeds()}")
    print(f"calculate_total_revenue: {model.calculate_total_revenue()}")
    print(f"calculate_annual_revenue_distribution: {model.calculate_annual_revenue_distribution()}")
    print(f"calculate_annual_operating_expenses: {model.calculate_annual_operating_expenses()}")
    print(f"calculate_annual_cash_flow: {model.calculate_net_annual_cash_flow()}")
    print(f"calculate_mortgage_remain_balance_in_exit: {model.calculate_mortgage_remain_balance_in_exit()}")
    print(f"calculate_constructor_index_linked_compensation: {model.calculate_constructor_index_linked_compensation()}")
    print(f"calculate_total_expenses: {model.calculate_total_expenses()}")
    print(f"calculate_equity_needed_for_purchase: {model.calculate_total_equity_needed_for_purchase()}")
    print(f"calculate_contractor_payments: {model.calculate_equity_payments()}")
    print(f"calculate_annual_expenses_distribution: {model.calculate_annual_expenses_distribution()}")
    print(f"calculate_monthly_property_management_fees: {model.calculate_monthly_property_management_fees()}")
    print(f"calculate_annual_property_management_fees: {model.calculate_annual_property_management_fees()}")
    print(f"calculate_net_profit: {model.calculate_net_profit()}")
    print(f"calculate_capital_gain_tax: {model.calculate_capital_gain_tax()}")
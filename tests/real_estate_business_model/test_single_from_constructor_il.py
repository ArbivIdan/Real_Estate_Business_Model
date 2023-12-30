import unittest

from src.business_models.Israel.single_from_constructor_il import SingleFromConstructorIL
from src.business_models.real_estate_property import RealEstateProperty
from src.investors.Israel.real_estate_investment_type import RealEstateInvestmentType
from src.investors.real_estate_investor import RealEstateInvestor
from src.investors.real_estate_investors_portfolio import RealEstateInvestorsPortfolio
from src.mortgage.mortgage_pipeline import MortgagePipeline
from src.mortgage.mortgage_tracks.constant_linked import ConstantLinked
import numpy as np

from unittest.mock import MagicMock

from src.mortgage.mortgage_tracks.constant_not_linked import ConstantNotLinked


class TestSingleFromConstructorIL(unittest.TestCase):

    def setUp(self):
        # Create mock objects for dependencies
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

        self.model = SingleFromConstructorIL(investors_portfolio=investors_portfolio,
                                             mortgage=mortgage,
                                             real_estate_property=property,
                                             years_to_exit=7,
                                             average_interest_in_exit={
                                                 mortgage.tracks[0].__class__: mortgage.tracks[0].interest_rate},
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

    # Financial Calculation

    def test_calculate_loan_to_cost(self):
        expected_loan_to_cost = 60
        self.assertEqual(expected_loan_to_cost, self.model.calculate_loan_to_cost())

    def test_calculate_loan_to_value(self):
        expected_loan_to_value = 60
        self.assertEqual(expected_loan_to_value, self.model.calculate_loan_to_value())

    def test_calculate_net_monthly_cash_flow(self):
        expected_net_monthly_cash_flow = -1271
        self.assertEqual(expected_net_monthly_cash_flow, self.model.calculate_net_monthly_cash_flow())

    def test_calculate_net_annual_cash_flow(self):
        expected_net_annual_cash_flow = -15252
        self.assertEqual(expected_net_annual_cash_flow, self.model.calculate_net_annual_cash_flow())

    def test_calculate_cash_on_cash(self):
        expected_cash_on_cash = -0.02
        self.assertEqual(expected_cash_on_cash, self.model.calculate_cash_on_cash())

    def test_calculate_annual_irr(self):
        expected_annual_irr = 7.43
        self.assertEqual(expected_annual_irr, self.model.calculate_annual_irr())

    def test_calculate_annual_cash_flow_distribution(self):
        expected_annual_cash_flow_distribution = [-424940, 0, -409157, -15240, -15240, -15240, -15240, 1360160]
        self.assertEqual(expected_annual_cash_flow_distribution, self.model.calculate_annual_cash_flow_distribution())

    def test_calculate_roi(self):
        expected_roi = 0.71
        self.assertEqual(expected_roi, self.model.calculate_roi())

    def test_calculate_monthly_noi(self):
        expected_monthly_noi = 3714
        self.assertEqual(expected_monthly_noi, self.model.calculate_monthly_noi())

    def test_calculate_annual_noi(self):
        expected_annual_noi = 44568
        self.assertEqual(expected_annual_noi, self.model.calculate_annual_noi())

    def test_calculate_annual_cap_rate(self):
        expected_annual_cap_rate = 2.41
        self.assertEqual(expected_annual_cap_rate, self.model.calculate_annual_cap_rate())

    def test_calculate_annual_gross_yield(self):
        expected_annual_gross_yield = 2.66
        self.assertEqual(expected_annual_gross_yield, self.model.calculate_annual_gross_yield())

    def test_calculate_net_profit(self):
        expected_net_profit = 579442
        self.assertEqual(expected_net_profit, self.model.calculate_net_profit())

    def test_estimate_property_value_with_noi(self):
        expected_property_value_with_noi = 1849295
        self.assertEqual(expected_property_value_with_noi, self.model.estimate_property_value_with_noi())

    # Purchase

    def test_calculate_broker_purchase_cost(self):
        expected_calculate_broker_purchase_cost = 0
        self.assertEqual(expected_calculate_broker_purchase_cost, self.model.calculate_broker_purchase_cost())

    def test_calculate_closing_costs(self):
        expected_calculate_closing_costs = 54940
        self.assertEqual(expected_calculate_closing_costs, self.model.calculate_closing_costs())

    def test_calculate_price_per_meter(self):
        expected_calculate_price_per_meter = 27820
        self.assertEqual(expected_calculate_price_per_meter, self.model.calculate_price_per_meter())

    def test_calculate_total_renovation_expenses(self):
        expected_calculate_total_renovation_expenses = 0
        self.assertEqual(expected_calculate_total_renovation_expenses, self.model.calculate_total_renovation_expenses())

    def test_calculate_purchase_additional_transactions_cost(self):
        expected_calculate_purchase_additional_transactions_cost = 1340
        self.assertEqual(expected_calculate_purchase_additional_transactions_cost,
                         self.model.calculate_purchase_additional_transactions_cost())

    def test_calculate_total_equity_needed_for_purchase(self):
        expected_calculate_total_equity_needed_for_purchase = 818857
        self.assertEqual(expected_calculate_total_equity_needed_for_purchase,
                         self.model.calculate_total_equity_needed_for_purchase())

    def test_calculate_equity_payments(self):
        expected_calculate_equity_payments = [424940, 0, 393917]
        self.assertEqual(expected_calculate_equity_payments, self.model.calculate_equity_payments())

    # Taxes

    def test_calculate_purchase_tax(self):
        expected_calculate_purchase_tax = 0
        self.assertEqual(expected_calculate_purchase_tax, self.model.calculate_purchase_tax())

    def test_calculate_monthly_rental_property_taxes(self):
        expected_calculate_monthly_rental_property_taxes = 0
        self.assertEqual(expected_calculate_monthly_rental_property_taxes,
                         self.model.calculate_monthly_rental_property_taxes())

    def test_calculate_annual_rental_property_taxes(self):
        expected_calculate_annual_rental_property_taxes = 0
        self.assertEqual(expected_calculate_annual_rental_property_taxes,
                         self.model.calculate_annual_rental_property_taxes())

    def test_calculate_capital_gain_tax(self):
        expected_calculate_capital_gain_tax = 0
        self.assertEqual(expected_calculate_capital_gain_tax, self.model.calculate_capital_gain_tax())

    # Holding

    def test_calculate_monthly_property_management_fees(self):
        expected_calculate_monthly_property_management_fees = 0
        self.assertEqual(expected_calculate_monthly_property_management_fees,
                         self.model.calculate_monthly_property_management_fees())

    def test_calculate_annual_property_management_fees(self):
        expected_calculate_annual_property_management_fees = 0
        self.assertEqual(expected_calculate_annual_property_management_fees,
                         self.model.calculate_annual_property_management_fees())

    def test_calculate_monthly_insurances_expenses(self):
        expected_calculate_monthly_insurances_expenses = 58
        self.assertEqual(expected_calculate_monthly_insurances_expenses,
                         self.model.calculate_monthly_insurances_expenses())

    def test_calculate_annual_insurances_expenses(self):
        expected_calculate_annual_insurances_expenses = 700
        self.assertEqual(expected_calculate_annual_insurances_expenses,
                         self.model.calculate_annual_insurances_expenses())

    def test_calculate_monthly_maintenance_and_repairs(self):
        expected_calculate_monthly_maintenance_and_repairs = 164
        self.assertEqual(expected_calculate_monthly_maintenance_and_repairs,
                         self.model.calculate_monthly_maintenance_and_repairs())

    def test_calculate_annual_maintenance_and_repairs(self):
        expected_calculate_annual_maintenance_and_repairs = 1968
        self.assertEqual(expected_calculate_annual_maintenance_and_repairs,
                         self.model.calculate_annual_maintenance_and_repairs())

    def test_calculate_annual_vacancy_cost(self):
        expected_calculate_annual_vacancy_cost = 1968
        self.assertEqual(expected_calculate_annual_vacancy_cost, self.model.calculate_annual_vacancy_cost())

    def test_calculate_monthly_operating_expenses(self):
        expected_calculate_monthly_operating_expenses = 386
        self.assertEqual(expected_calculate_monthly_operating_expenses,
                         self.model.calculate_monthly_operating_expenses())

    def test_calculate_annual_operating_expenses(self):
        expected_calculate_annual_operating_expenses = 4632
        self.assertEqual(expected_calculate_annual_operating_expenses, self.model.calculate_annual_operating_expenses())

    # Holding Revenues

    def test_calculate_annual_rent_income(self):
        expected_calculate_annual_rent_income = 49200
        self.assertEqual(expected_calculate_annual_rent_income, self.model.calculate_annual_rent_income())

    # Selling

    def test_calculate_annual_estimated_property_value(self):
        expected_calculate_annual_estimated_property_value = [1850000, 1915563, 1982770, 2051644, 2122210, 2194493,
                                                              2268518, 2344310]
        self.assertEqual(expected_calculate_annual_estimated_property_value,
                         self.model.calculate_annual_estimated_property_value())

    def test_calculate_estimated_property_value(self):
        expected_calculate_estimated_property_value = 2353717
        self.assertEqual(expected_calculate_estimated_property_value, self.model.calculate_estimated_property_value())

    def test_estimate_sale_price(self):
        expected_estimate_sale_price = 2353717
        self.assertEqual(expected_estimate_sale_price, self.model.estimate_sale_price())

    def test_calculate_selling_expenses(self):
        expected_calculate_selling_expenses = 0
        self.assertEqual(expected_calculate_selling_expenses, self.model.calculate_selling_expenses())

    def test_calculate_sale_proceeds(self):
        expected_calculate_sale_proceeds = 2353717
        self.assertEqual(expected_calculate_sale_proceeds, self.model.calculate_sale_proceeds())

    def test_calculate_mortgage_remain_balance_in_exit(self):
        expected_calculate_mortgage_remain_balance_in_exit = 993557
        self.assertEqual(expected_calculate_mortgage_remain_balance_in_exit,
                         self.model.calculate_mortgage_remain_balance_in_exit())

    # General

    def test_calculate_total_revenue(self):
        expected_calculate_total_revenue = 2599717
        self.assertEqual(expected_calculate_total_revenue, self.model.calculate_total_revenue())

    def test_calculate_total_expenses(self):
        expected_calculate_total_expenses = 2020275
        self.assertEqual(expected_calculate_total_expenses, self.model.calculate_total_expenses())

    def test_calculate_annual_revenue_distribution(self):
        expected_calculate_annual_revenue_distribution = [0, 0, 49200, 49200, 49200, 49200, 49200, 2353717]
        self.assertEqual(expected_calculate_annual_revenue_distribution,
                         self.model.calculate_annual_revenue_distribution())

    def test_calculate_annual_expenses_distribution(self):
        expected_calculate_annual_expenses_distribution = [424940, 0, 458357, 64440, 64440, 64440, 64440, 993557]
        self.assertEqual(expected_calculate_annual_expenses_distribution,
                         self.model.calculate_annual_expenses_distribution())

    def test_get_annual_property_remain_balances(self):
        expected_get_annual_property_remain_balances = [1108253.1, 1108253.1, 1108253, 1086889, 1064764, 1041853,
                                                        1018127, 993557]
        self.assertEqual(expected_get_annual_property_remain_balances, self.model.get_annual_property_remain_balances())


if __name__ == "__main__":
    unittest.main()

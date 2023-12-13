from typing import List

from src.real_estate_financial_model.single_house_israel_model import SingleHouseIsraelModel


class SingleHouseSecondHandIL(SingleHouseIsraelModel):
    def calculate_total_expenses(self) -> int:
        return (self.calculate_total_equity_needed_for_purchase() +
                round(self.years_to_exit * self.calculate_annual_operating_expenses()) +
                self.calculate_selling_expenses() +
                self.mortgage.calculate_total_cost_of_borrowing(self.years_to_exit, self.average_interest_in_exit) +
                self.calculate_capital_gain_tax() +
                self.calculate_mortgage_remain_balance_in_exit())

    def calculate_annual_expenses_distribution(self) -> List[float]:
        annual_distribution_operating_expenses = [self.calculate_annual_operating_expenses() for _ in
                                                  range(self.years_to_exit)] + [0]

        estimated_mortgage_monthly_payments = self.mortgage.get_annual_payments()[:self.years_to_exit] + [0]

        equity_distribution_to_property_purchase = self.calculate_equity_payments() + [0] * self.years_to_exit

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

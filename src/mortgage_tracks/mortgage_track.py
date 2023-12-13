from abc import ABC, abstractmethod
import numpy_financial as npf
import matplotlib
from src.mortgage_utils.mortgage_plotter_util import plot_monthly_payments, plot_principal_and_interest_payments
from src.mortgage_utils.mortgage_printer_util import plot_mortgage_monthly_payments
from typing import Optional, List

matplotlib.use('TkAgg')
from src.constants import Constants


class MortgageTrack(ABC):

    def __init__(self, interest_rate: float, num_payments: int, initial_loan_amount: float, linked_index: Optional[List[float]] = None,
                 forecasting_interest_rate: Optional[List[float]] = None, average_interest_when_taken: Optional[float] = None, interest_only_period: int = 0):
        self.interest_rate = interest_rate
        self.num_payments = num_payments
        self.initial_loan_amount = initial_loan_amount
        self.linked_index = linked_index if linked_index else [0.0] * 360
        self.forecasting_interest_rate = forecasting_interest_rate if forecasting_interest_rate else [0.0] * 360
        self.average_interest_when_taken = average_interest_when_taken if average_interest_when_taken else interest_rate
        self.interest_only_period = interest_only_period

    def get_principal_payments(self):
        return self._calculate_payments()[0]

    def get_interest_payments(self):
        return self._calculate_payments()[1]

    def get_monthly_payments(self):
        return self._calculate_payments()[2]

    def get_remaining_balances(self):
        return self._calculate_payments()[3]

    def get_total_principal_paid(self):
        return self._calculate_payments()[4]

    def get_total_interest_paid(self):
        return self._calculate_payments()[5]


    def calculate_initial_monthly_payment(self):
        #TODO: Check how its work with the interest only period
        return npf.pmt(self.interest_rate / Constants.MONTHS_IN_YEAR, self.num_payments, -self.initial_loan_amount)

    def calculate_loan_yearly_irr(self):
        # Yearly IRR = Month IRR * 12 Months * 100 (Percentage) * -1 (Bank Investment)
        monthly_cash_flow = [-self.initial_loan_amount] + self.get_monthly_payments()
        return npf.irr(monthly_cash_flow) * Constants.MONTHS_IN_YEAR * 100 * -1

    def plot_monthly_payments(self) -> None:
        """

        :return:
        """
        plot_monthly_payments(self.num_payments, self.get_monthly_payments())

    def plot_principal_and_interest_payments(self) -> None:
        """

        :return:
        """
        plot_principal_and_interest_payments(self.num_payments, self.get_principal_payments(), self.get_interest_payments())

    def _calculate_payments(self):
        # Initialize variables
        principal_payments, interest_payments, monthly_payments, remaining_balances = [], [], [], []
        total_principal_paid, total_interest_paid = 0, 0

        remaining_balance = self.initial_loan_amount
        interest_rate = self.interest_rate

        monthly_interest = interest_rate / Constants.MONTHS_IN_YEAR

        for i in range(self.interest_only_period):
            interest_payment = round(remaining_balance * monthly_interest, 2)
            principal_payment = 0
            total_interest_paid += interest_payment
            principal_payments.append(principal_payment)
            interest_payments.append(interest_payment)
            remaining_balances.append(remaining_balance)
            monthly_payments.append(principal_payment + interest_payment)

        num_payments = self.num_payments - self.interest_only_period

        # Calculate and display the breakdown for each month
        for period in range(1, num_payments + 1):
            # total_linked_index_paid += remaining_balance * self.consumer_price_index[period-1]
            remaining_balance = remaining_balance * (1 + self.linked_index[period - 1])
            interest_rate = interest_rate * (1 + self.forecasting_interest_rate[period - 1])

            interest_payment = remaining_balance * monthly_interest
            principal_payment = npf.pmt(monthly_interest, num_payments - (period - 1),
                                        -remaining_balance) - interest_payment
            remaining_balance -= principal_payment

            total_principal_paid += principal_payment
            total_interest_paid += interest_payment

            principal_payment, interest_payment, remaining_balance = round(principal_payment, 2), round(
                interest_payment, 2), round(remaining_balance, 2)

            principal_payments.append(principal_payment)
            interest_payments.append(interest_payment)
            remaining_balances.append(remaining_balance)
            monthly_payments.append(principal_payment + interest_payment)

        return principal_payments, interest_payments, monthly_payments, remaining_balances, total_principal_paid, total_interest_paid

    def calculate_highest_monthly_payment(self):
        return max(self.get_monthly_payments())

    def calculate_total_interest_payment(self):
        return sum(self.get_interest_payments())

    def calculate_linked_index_payment(self):
        return self.calculate_total_repayment() - self.calculate_total_interest_payment() - self.initial_loan_amount

    def loan_cost(self):
        return self.calculate_total_repayment() / self.initial_loan_amount

    def calculate_total_repayment(self):
        return sum(self.get_monthly_payments())

    def print_payments(self):
        plot_mortgage_monthly_payments(self.num_payments,
                                       self.get_principal_payments(),
                                       self.get_interest_payments(),
                                       self.get_remaining_balances())

    @abstractmethod
    def calculate_early_payment_fee(self, num_of_months: int, average_interest_in_early_payment: float):
        pass

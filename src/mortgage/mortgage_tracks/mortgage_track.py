from abc import ABC, abstractmethod
import numpy_financial as npf
import matplotlib
from src.mortgage.mortgage_utils.mortgage_plotter_util import plot_monthly_payments, \
    plot_principal_and_interest_payments, plot_remain_balances
from src.mortgage.mortgage_utils.mortgage_printer_util import plot_mortgage_monthly_payments
from typing import Optional, List, Tuple

matplotlib.use('TkAgg')
from src.mortgage.mortgage_constants import MortgageConstants


class MortgageTrack(ABC):

    def __init__(self, interest_rate: float, num_payments: int, initial_loan_amount: int, linked_index: Optional[List[float]] = None,
                 forecasting_interest_rate: Optional[List[float]] = None, average_interest_when_taken: Optional[float] = None, interest_only_period: int = 0):
        self.interest_rate = interest_rate
        self.num_payments = num_payments
        self.initial_loan_amount = initial_loan_amount
        self.linked_index = linked_index if linked_index else [0.0] * 360
        self.forecasting_interest_rate = forecasting_interest_rate if forecasting_interest_rate else [0.0] * 360
        self.average_interest_when_taken = average_interest_when_taken if average_interest_when_taken else interest_rate
        self.interest_only_period = interest_only_period

    def get_principal_payments(self) -> List[int]:
        """
        Get the list of principal payments over the loan term.

        :return: A list of principal payments.
        """
        return self._calculate_payments()[0]

    def get_interest_payments(self) -> List[int]:
        """
        Get the list of interest payments over the loan term.

        :return: A list of interest payments.
        """
        return self._calculate_payments()[1]

    def get_monthly_payments(self) -> List[int]:
        """
        Get the list of monthly payments over the loan term.

        :return: A list of monthly payments.
        """
        return self._calculate_payments()[2]

    def get_remaining_balances(self) -> List[int]:
        """
        Get the list of remaining balances over the loan term.

        :return: A list of remaining balances.
        """
        return self._calculate_payments()[3]

    def get_total_principal_paid(self) -> int:
        """
        Get the total amount of principal paid over the loan term.

        :return: The total amount of principal paid.
        """
        return self._calculate_payments()[4]

    def get_total_interest_paid(self) -> int:
        """
        Get the total amount of interest paid over the loan term.

        :return: The total amount of interest paid.
        """
        return self._calculate_payments()[5]


    def calculate_initial_monthly_payment(self) -> int:
        #TODO: Check how its work with the interest only period
        return npf.pmt(self.interest_rate / MortgageConstants.MONTHS_IN_YEAR, self.num_payments, -self.initial_loan_amount)

    def calculate_loan_annual_irr(self) -> float:
        """
        Calculate the annual Internal Rate of Return (IRR) for the loan.

        The annual IRR is calculated based on the monthly cash flows, including the initial loan amount and monthly payments.

        :return: The calculated yearly IRR as a percentage.
        """
        # Yearly IRR = Month IRR * 12 Months * 100 (Percentage) * -1 (Bank Investment)
        monthly_cash_flow = [-self.initial_loan_amount] + self.get_monthly_payments()
        return npf.irr(monthly_cash_flow) * MortgageConstants.MONTHS_IN_YEAR * 100 * -1

    def plot_monthly_payments(self) -> None:
        """
        Plot the monthly payments over the loan term.

        Uses the utility function `plot_monthly_payments` to create the plot.

        :return: None
        """
        plot_monthly_payments(self.num_payments, self.get_monthly_payments())

    def plot_principal_and_interest_payments(self) -> None:
        """
        Plot the principal and interest payments over the loan term.

        Uses the utility function `plot_principal_and_interest_payments` to create the plot.

        :return: None
        """
        plot_principal_and_interest_payments(self.num_payments, self.get_principal_payments(), self.get_interest_payments())

    def plot_remain_balances(self) -> None:
        plot_remain_balances(self.get_remaining_balances())

    def _calculate_payments(self) -> Tuple[List[int], List[int], List[int], List[int], int, int]:
        """
        Calculate principal, interest, monthly payments, and remaining balances over the loan term.

        This private method performs the calculation for principal and interest payments for each month of the loan term.

        :return: A tuple containing lists of principal payments, interest payments, monthly payments, remaining balances, total principal paid, and total interest paid.
        """
        # Initialize variables
        principal_payments, interest_payments, monthly_payments, remaining_balances = [], [], [], []
        total_principal_paid, total_interest_paid = 0, 0

        # Initial values for the first period
        remaining_balance = self.initial_loan_amount
        interest_rate = self.interest_rate

        # Monthly interest rate
        monthly_interest = interest_rate / MortgageConstants.MONTHS_IN_YEAR

        # Calculate interest-only period
        for i in range(self.interest_only_period):
            interest_payment = round(remaining_balance * monthly_interest, 2)
            principal_payment = 0
            total_interest_paid += interest_payment
            principal_payments.append(principal_payment)
            interest_payments.append(interest_payment)
            remaining_balances.append(remaining_balance)
            monthly_payments.append(principal_payment + interest_payment)

        # Calculate principal and interest payments for the remaining term
        num_payments = self.num_payments - self.interest_only_period
        for period in range(1, num_payments + 1):
            # Update remaining balance and interest rate based on indices
            remaining_balance = remaining_balance * (1 + self.linked_index[period - 1])
            interest_rate = interest_rate * (1 + self.forecasting_interest_rate[period - 1])

            # Calculate interest and principal payments for the current period
            interest_payment = remaining_balance * monthly_interest
            principal_payment = npf.pmt(monthly_interest, num_payments - (period - 1),
                                        -remaining_balance) - interest_payment
            remaining_balance -= principal_payment

            # Update total payments
            total_principal_paid += principal_payment
            total_interest_paid += interest_payment

            # Round values and append to lists
            principal_payment, interest_payment, remaining_balance = round(principal_payment, 2), round(
                interest_payment, 2), round(remaining_balance, 2)
            principal_payments.append(principal_payment)
            interest_payments.append(interest_payment)
            remaining_balances.append(remaining_balance)
            monthly_payments.append(principal_payment + interest_payment)

        return principal_payments, interest_payments, monthly_payments, remaining_balances, total_principal_paid, total_interest_paid

    def calculate_highest_monthly_payment(self) -> int:
        """
        Calculate the highest monthly payment over the loan term.

        :return: The highest monthly payment.
        """
        return max(self.get_monthly_payments())

    def calculate_total_interest_payment(self) -> int:
        """
        Calculate the total interest payments over the loan term.

        :return: The total interest payments.
        """
        return sum(self.get_interest_payments())

    def calculate_linked_index_payment(self) -> int:
        """
        Calculate the total payments related to the linked index (excluding principal and interest).

        :return: The calculated total linked index payments.
        """
        return self.calculate_total_repayment() - self.calculate_total_interest_payment() - self.initial_loan_amount

    def loan_cost(self) -> float:
        """
        Calculate the loan cost, which is the ratio of total repayment to the initial loan amount.

        :return: The calculated loan cost.
        """
        return self.calculate_total_repayment() / self.initial_loan_amount

    def calculate_total_repayment(self) -> int:
        """
        Calculate the total repayment over the loan term.

        :return: The total repayment.
        """
        return sum(self.get_monthly_payments())

    def print_payments(self) -> None:
        """
        Print a plot of mortgage monthly payments over the loan term.

        Uses the utility function `plot_mortgage_monthly_payments` to create the plot.

        :return: None
        """
        plot_mortgage_monthly_payments(self.num_payments,
                                       self.get_principal_payments(),
                                       self.get_interest_payments(),
                                       self.get_remaining_balances())

    @abstractmethod
    def calculate_early_payment_fee(self, num_of_months: int, average_interest_in_early_payment: float) -> int:
        """
        Calculate the early payment fee.

        :param num_of_months: Number of months for which early payment is considered.
        :param average_interest_in_early_payment: Average interest rate during early payment.
        :return: The calculated early payment fee.
        """
        pass

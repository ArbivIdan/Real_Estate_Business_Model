from src.mortgage_tracks.mortgage_track import MortgageTrack
from src.mortgage_utils.mortgage_financial_utils import calculate_early_payment_fee
from typing import Optional, List


class ConstantNotLinked(MortgageTrack):
    def __init__(self, interest_rate: float, num_payments: int, initial_loan_amount: float,
                 average_interest_when_taken: Optional[float] = None, interest_only_period: int = 0):
        super().__init__(interest_rate, num_payments, initial_loan_amount, average_interest_when_taken=average_interest_when_taken, interest_only_period=interest_only_period)

    def calculate_early_payment_fee(self, num_of_months: int, average_interest_in_early_payment: float) -> int:
        if num_of_months < 0 or average_interest_in_early_payment < 0:
            raise ValueError(
                f"Function arguments must be non-negative: number of months: {num_of_months}, average interest in early payment: {average_interest_in_early_payment}")
        return calculate_early_payment_fee(average_interest_in_early_payment,
                                           self.get_monthly_payments()[num_of_months:],
                                           self.interest_rate, self.average_interest_when_taken, -1)




if __name__ == "__main__":
    cons = ConstantNotLinked(interest_rate=2.5 / 100,
                                                  num_payments=360,
                                                  initial_loan_amount= 0.6,
                                                  interest_only_period=5)
    cons.print_payments()
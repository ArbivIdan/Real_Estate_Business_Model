from src.mortgage.mortgage_tracks.mortgage_track import MortgageTrack
from typing import List, Optional

class Prime(MortgageTrack):
    def __init__(self, interest_rate: float, num_payments: int, initial_loan_amount: int,
                 forecasting_interest_rate: List[float], average_interest_when_taken: Optional[float] = None, interest_only_period: int = 0):
        super().__init__(interest_rate, num_payments, initial_loan_amount,
                         forecasting_interest_rate=forecasting_interest_rate, average_interest_when_taken=average_interest_when_taken, interest_only_period=interest_only_period)

    def calculate_early_payment_fee(self, num_of_months: int, average_interest_in_early_payment: float) -> int:
        """
        Calculate the early payment fee.

        :param num_of_months: Number of months for which early payment is considered.
        :param average_interest_in_early_payment: Average interest rate during early payment.
        :return: The calculated early payment fee.
        """
        if num_of_months < 0 or average_interest_in_early_payment < 0:
            raise ValueError(f"Function arguments must be non-negative: number of months: {num_of_months}, average interest in early payment: {average_interest_in_early_payment}")
        return 0

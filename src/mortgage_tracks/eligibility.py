from src.mortgage_tracks.mortgage_track import MortgageTrack
from typing import List, Optional


class Eligibility(MortgageTrack):
    def __init__(self, interest_rate: float, num_payments: int, initial_loan_amount: float,
                 linked_index: List[float], average_interest_when_taken: Optional[float] = None):
        super().__init__(interest_rate, num_payments, initial_loan_amount, linked_index=linked_index, average_interest_when_taken=average_interest_when_taken)

    def calculate_early_payment_fee(self, num_of_months: int, average_interest_in_early_payment: float) -> int:
        if num_of_months < 0 or average_interest_in_early_payment < 0:
            raise ValueError(
                f"Function arguments must be non-negative: number of months: {num_of_months}, average interest in early payment: {average_interest_in_early_payment}")
        return 0

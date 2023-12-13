import unittest
from src.mortgage_tracks.constant_not_linked import ConstantNotLinked
from unittest.mock import patch
import numpy as np

class TestConstantNotLinked(unittest.TestCase):

    def setUp(self):
        # Create an instance of MortgageTrack for testing
        self.mortgage_track = ConstantNotLinked(
            interest_rate=4 / 100,
            num_payments=360,
            initial_loan_amount=100_000,
        )

    def test_calculate_early_payment_fee(self):
        # Ensure that ValueError is raised when the number of months is negative
        with self.assertRaises(ValueError):
            self.mortgage_track.calculate_early_payment_fee(num_of_months=-1, average_interest_in_early_payment=0.02)

        with self.assertRaises(ValueError):
            self.mortgage_track.calculate_early_payment_fee(num_of_months=0, average_interest_in_early_payment=-0.02)

        self.assertEqual(29164, self.mortgage_track.calculate_early_payment_fee(num_of_months=0,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(26344, self.mortgage_track.calculate_early_payment_fee(num_of_months=24,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(19490, self.mortgage_track.calculate_early_payment_fee(num_of_months=84,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(13114, self.mortgage_track.calculate_early_payment_fee(num_of_months=144,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(7533, self.mortgage_track.calculate_early_payment_fee(num_of_months=204,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(3154, self.mortgage_track.calculate_early_payment_fee(num_of_months=264,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(498, self.mortgage_track.calculate_early_payment_fee(num_of_months=324,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=360,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=500,
                                                                            average_interest_in_early_payment=2 / 100))

    def test_calculate_initial_monthly_payment(self):
        # Ensure that the calculated initial monthly payment is as expected
        expected_payment = 477  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.calculate_initial_monthly_payment()), expected_payment,
                               places=2)

    # @patch('numpy_financial.irr')
    def test_calculate_loan_yearly_irr(self):
        # Mock the numpy_financial.irr function to return a fixed value for testing
        # mock_irr.return_value = 0.04
        # Ensure that the calculated yearly IRR is as expected
        expected_irr = -4.00  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.calculate_loan_yearly_irr(), 2), expected_irr, places=1)

    def test_calculate_highest_monthly_payment(self):
        # Ensure that the calculated highest monthly payment is as expected
        expected_highest_payment = 477  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.calculate_highest_monthly_payment()), expected_highest_payment,
                               places=2)

    def test_calculate_total_interest_payment(self):
        # Ensure that the calculated total interest payment is as expected
        expected_total_interest = 71870  # replace with the actual expected value
        self.assertAlmostEqual(np.ceil(self.mortgage_track.calculate_total_interest_payment()), expected_total_interest,
                               places=2)

    def test_calculate_linked_index_payment(self):
        # Ensure that the calculated linked index payment is as expected
        expected_linked_index_payment = 0  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.calculate_linked_index_payment()), expected_linked_index_payment,
                               places=2)

    def test_loan_cost(self):
        # Ensure that the calculated loan cost is as expected
        expected_loan_cost = 1.72  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.loan_cost(), 2), expected_loan_cost, places=5)

    def test_calculate_total_repayment(self):
        # Ensure that the calculated total repayment is as expected
        expected_total_repayment = 171_870  # replace with the actual expected value
        self.assertAlmostEqual(np.ceil(self.mortgage_track.calculate_total_repayment()), expected_total_repayment, places=2)


if __name__ == "__main__":
    unittest.main()


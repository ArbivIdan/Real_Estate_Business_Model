import unittest
from src.mortgage_tracks.eligibility import Eligibility
import numpy as np

class TestConstantLinked(unittest.TestCase):

    def setUp(self):
        # Create an instance of MortgageTrack for testing
        self.mortgage_track = Eligibility(
            interest_rate=4 / 100,
            num_payments=360,
            initial_loan_amount=100_000,
            linked_index= [2 / (12* 100) for _ in range(360)]
        )

    def test_calculate_early_payment_fee(self):
        # Ensure that ValueError is raised when the number of months is negative
        with self.assertRaises(ValueError):
            self.mortgage_track.calculate_early_payment_fee(num_of_months=-1, average_interest_in_early_payment=0.02)

        with self.assertRaises(ValueError):
            self.mortgage_track.calculate_early_payment_fee(num_of_months=0, average_interest_in_early_payment=-0.02)

        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=0,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=24,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=84,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=144,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=204,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=264,
                                                                            average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_track.calculate_early_payment_fee(num_of_months=324,
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
        expected_irr = -6.01  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.calculate_loan_yearly_irr(), 2), expected_irr, places=1)

    def test_calculate_highest_monthly_payment(self):
        # Ensure that the calculated highest monthly payment is as expected
        expected_highest_payment = 869  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.calculate_highest_monthly_payment()), expected_highest_payment,
                               places=2)

    def test_calculate_total_interest_payment(self):
        # Ensure that the calculated total interest payment is as expected
        expected_total_interest = 90_468  # replace with the actual expected value
        self.assertAlmostEqual(np.ceil(self.mortgage_track.calculate_total_interest_payment()), expected_total_interest,
                               places=2)

    def test_calculate_linked_index_payment(self):
        # Ensure that the calculated linked index payment is as expected
        expected_linked_index_payment = 45_159  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.calculate_linked_index_payment()), expected_linked_index_payment,
                               places=2)

    def test_loan_cost(self):
        # Ensure that the calculated loan cost is as expected
        expected_loan_cost = 2.36  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_track.loan_cost(), 2), expected_loan_cost, places=5)

    def test_calculate_total_repayment(self):
        # Ensure that the calculated total repayment is as expected
        expected_total_repayment = 235_627  # replace with the actual expected value
        self.assertAlmostEqual(np.ceil(self.mortgage_track.calculate_total_repayment()), expected_total_repayment, places=2)


if __name__ == "__main__":
    unittest.main()


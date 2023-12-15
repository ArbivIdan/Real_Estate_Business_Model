import unittest
from src.mortgage.mortgage_pipeline import MortgagePipeline
from src.mortgage.mortgage_tracks.constant_not_linked import ConstantNotLinked
from src.mortgage.mortgage_tracks.constant_linked import ConstantLinked
import numpy as np


class TestMortgagePipeline(unittest.TestCase):

    def setUp(self):
        # Create an instance of MortgageTrack for testing
        constant_link = ConstantLinked(
            interest_rate=4 / 100,
            num_payments=360,
            initial_loan_amount=100_000,
            linked_index=[0.02 / 12 for _ in range(360)]
        )

        constant_not_linked = ConstantNotLinked(
            interest_rate=5 / 100,
            num_payments=120,
            initial_loan_amount=100_000,
        )

        self.mortgage_pipeline = MortgagePipeline(
            constant_link,
            constant_not_linked
        )

    def test_calculate_early_payment_fee(self):
        # Ensure that ValueError is raised when the number of months is negative
        with self.assertRaises(ValueError):
            self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=-1, average_interest_in_early_payment=0.02)

        with self.assertRaises(ValueError):
            self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=0, average_interest_in_early_payment=-0.02)

        self.assertEqual(44436, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=0,
                                                                                   average_interest_in_early_payment=2 / 100))
        self.assertEqual(36586, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=24,
                                                                                   average_interest_in_early_payment=2 / 100))
        self.assertEqual(14792, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=84,
                                                                                   average_interest_in_early_payment=2 / 100))
        self.assertEqual(9180, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=144,
                                                                                  average_interest_in_early_payment=2 / 100))
        self.assertEqual(5273, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=204,
                                                                                  average_interest_in_early_payment=2 / 100))
        self.assertEqual(2208, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=264,
                                                                                  average_interest_in_early_payment=2 / 100))
        self.assertEqual(349, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=324,
                                                                                 average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=360,
                                                                               average_interest_in_early_payment=2 / 100))
        self.assertEqual(0, self.mortgage_pipeline.calculate_early_payment_fee(num_of_months=500,
                                                                               average_interest_in_early_payment=2 / 100))

    def test_calculate_initial_monthly_payment(self):
        # Ensure that the calculated initial monthly payment is as expected
        expected_payment = 1538  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_pipeline.calculate_initial_monthly_payment()), expected_payment,
                               places=2)

    # @patch('numpy_financial.irr')
    def test_calculate_loan_yearly_irr(self):
        # Mock the numpy_financial.irr function to return a fixed value for testing
        # mock_irr.return_value = 0.04
        # Ensure that the calculated yearly IRR is as expected
        expected_irr = -5.74  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_pipeline.calculate_loan_yearly_irr(), 2), expected_irr, places=1)

    def test_calculate_highest_monthly_payment(self):
        # Ensure that the calculated highest monthly payment is as expected
        expected_highest_payment = 1644  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_pipeline.calculate_highest_monthly_payment()),
                               expected_highest_payment,
                               places=2)

    def test_calculate_total_interest_payment(self):
        # Ensure that the calculated total interest payment is as expected
        expected_total_interest = 117_747  # replace with the actual expected value
        self.assertAlmostEqual(np.ceil(self.mortgage_pipeline.calculate_total_interest_payment()),
                               expected_total_interest,
                               places=2)

    def test_calculate_linked_index_payment(self):
        # Ensure that the calculated linked index payment is as expected
        expected_linked_index_payment = 45_159  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_pipeline.calculate_linked_index_payment()),
                               expected_linked_index_payment,
                               places=2)

    def test_loan_cost(self):
        # Ensure that the calculated loan cost is as expected
        expected_loan_cost = 1.81  # replace with the actual expected value
        self.assertAlmostEqual(round(self.mortgage_pipeline.total_loan_cost(), 2), expected_loan_cost, places=5)

    def test_calculate_total_repayment(self):
        # Ensure that the calculated total repayment is as expected
        expected_total_repayment = 362_906  # replace with the actual expected value
        self.assertAlmostEqual(np.ceil(self.mortgage_pipeline.get_total_payment()), expected_total_repayment,
                               places=2)

    def test_get_tracks_percentages_dic(self):
        expected_percentage_list = [0.5, 0.5]
        percentage_list = list(self.mortgage_pipeline.get_tracks_percentages_dic().values())
        self.assertEqual(expected_percentage_list, percentage_list)

    def test_calculate_num_payments(self):
        self.assertEqual(360, self.mortgage_pipeline.get_num_of_payments())

    def test_calculate_weighted_average_interest_rates(self):
        self.assertEqual(0.045, self.mortgage_pipeline.calculate_weighted_average_interest_rates())

    def test_calculate_normalize_resource_allocation(self):
        expected_normalize_resource_allocation = [0.31, 0.69]  # constant_link, constant_not_linked
        normalize_resource_allocation = [round(allocation, 2) for allocation in
                                         self.mortgage_pipeline.calculate_normalize_resource_allocation().values()]
        self.assertEqual(expected_normalize_resource_allocation, normalize_resource_allocation)

    def test_calculate_index_linkage_segmentation(self):
        # TODO:
        pass

    def test_calculate_interest_type_segmentation(self):
        # TODO:
        pass


if __name__ == "__main__":
    unittest.main()

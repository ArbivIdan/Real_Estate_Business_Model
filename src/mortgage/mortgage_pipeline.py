import numpy as np

from src.mortgage.mortgage_enums.interest_type import InterestType
from src.mortgage.mortgage_tracks.mortgage_track import MortgageTrack
from itertools import zip_longest
import numpy_financial as npf
import matplotlib
from src.mortgage.mortgage_tracks.eligibility import Eligibility
from src.mortgage.mortgage_utils.mortgage_financial_utils_il import calculate_discount_factor
from typing import List, Dict, Optional
from src.mortgage.mortgage_enums.linkage_type import LinkageType
from src.mortgage.mortgage_utils.mortgage_plotter_util import *
from src.mortgage.mortgage_utils.mortgage_printer_util import plot_mortgage_monthly_payments

matplotlib.use('TkAgg')


class MortgagePipeline:
    """
    A class representing a pipeline for managing and analyzing multiple MortgageTrack instances.

    The MortgagePipeline class is designed to handle various MortgageTrack instances and perform business logic
    related to mortgage calculations and analysis.

    Attributes:
        tracks (List[MortgageTrack]): A list containing MortgageTrack instances representing different mortgage tracks.
        total_loan_amount (Union[float, int]): The total initial loan amount across all mortgage tracks.

    Methods:
        - loan_cost(): Calculate the total loan cost considering the loan cost of each mortgage track and their percentages.
        - get_tracks_percentages_dic(): Get a dictionary with mortgage tracks as keys and their corresponding percentages.
        - get_principal_payments(): Get a list of principal payments across all tracks for specific time periods.
        - get_interest_payments(): Get a list of interest payments across all tracks for specific time periods.
        - get_monthly_payments(): Get a list of monthly payments across all tracks for specific time periods.
        - get_remain_balances(): Get a list of remaining balances across all tracks for specific time periods.
        - get_total_payment(): Get the total payment, which is the sum of total payments across all mortgage tracks.
        - calculate_highest_monthly_payment(): Calculate the highest monthly payment across all mortgage tracks.
        - calculate_initial_monthly_payment(): Calculate the initial monthly payment, which is the sum of initial monthly
          payments across all tracks.
        - calculate_loan_yearly_irr(): Calculate the yearly internal rate of return (IRR) for the mortgage.
        - calculate_num_payments(): Calculate the maximum number of payments among all mortgage tracks.
    """
    def __init__(self, *mortgage_tracks: MortgageTrack):
        """
        Initialize an instance of YourClassName with a variable number of MortgageTrack objects.

        :param mortgage_tracks: Variable number of MortgageTrack objects representing different mortgage tracks.
        :type mortgage_tracks: MortgageTrack
        """
        self.tracks = list(mortgage_tracks)
        self.total_initial_loan_amount = sum([track.initial_loan_amount for track in self.tracks])

    def calculate_total_interest_payment(self) -> int:
        """
        Calculate the total interest payments over the loan term.

        :return: The calculated total interest payments.
        """
        return sum(self.get_interest_payments())

    def calculate_linked_index_payment(self) -> int:
        """
        Calculate the total payments related to linked index (excluding principal and interest).

        :return: The calculated total linked index payments.
        """
        return self.get_total_payment() - self.calculate_total_interest_payment() - self.total_initial_loan_amount

    def get_tracks_percentages_dic(self) -> Dict[MortgageTrack, float]:
        """
        Get a dictionary with mortgage tracks as keys and their corresponding percentages of the total loan amount.

        :return: A dictionary with mortgage tracks as keys and their percentages.
        :rtype: Dict[MortgageTrack, float (between 0 and 1)]
        """
        tracks_percentages = [track.initial_loan_amount / self.total_initial_loan_amount for track in self.tracks]
        return {track: percentage for track, percentage in zip(self.tracks, tracks_percentages)}

    def get_principal_payments(self) -> List[float]:
        """
        Get a list of principal payments, where each element represents the sum of principal payments across all tracks
        for a monthly time period.

        :return: A list of principal payments.
        :rtype: List[float]
        """
        principal_payments_list = [track.get_principal_payments() for track in self.tracks]
        # Pad the lists with zeros and perform element-wise addition
        return [sum(x) for x in zip_longest(*principal_payments_list, fillvalue=0)]

    def get_annual_principal_payments(self) -> List[float]:
        """
        Get a list of principal payments, where each element represents the sum of principal payments across all tracks
        for a yearly time period.

        :return: A list of principal payments.
        :rtype: List[float]
        """
        return list(np.array(self.get_principal_payments()).reshape(-1, 12).sum(axis=1))

    def get_interest_payments(self) -> List[float]:
        """
        Get a list of interest payments, where each element represents the sum of interest payments across all tracks
        for a monthly time period.

        :return: A list of interest payments.
        :rtype: List[float]
        """
        interest_payments_list = [track.get_interest_payments() for track in self.tracks]
        # Pad the lists with zeros and perform element-wise addition
        return [sum(x) for x in zip_longest(*interest_payments_list, fillvalue=0)]

    def get_annual_interest_payments(self) -> List[float]:
        """
        Get a list of interest payments, where each element represents the sum of interest payments across all tracks
        for a yearly time period.

        :return: A list of interest payments.
        :rtype: List[float]
        """
        return list(np.array(self.get_interest_payments()).reshape(-1, 12).sum(axis=1))


    def get_monthly_payments(self) -> List[int]:
        """
        Get a list of monthly payments, where each element represents the sum of monthly payments across all tracks
        for a specific time period.

        :return: A list of monthly payments.
        :rtype: List[float]
        """
        monthly_payments_list = [track.get_monthly_payments() for track in self.tracks]
        # Pad the lists with zeros and perform element-wise addition
        return [round(sum(x)) for x in zip_longest(*monthly_payments_list, fillvalue=0)]

    def get_annual_payments(self) -> List[int]:
        """
        Get a list of annual payments, where each element represents the sum of annual payments across all tracks
        for a specific time period.

        :return: A list of monthly payments.
        :rtype: List[float]
        """
        return list(np.array(self.get_monthly_payments()).reshape(-1, 12).sum(axis=1))


    def get_remain_balances(self) -> List[int]:
        """
        Get a list of remaining balances, where each element represents the sum of remaining balances across all tracks
        for a month time period.

        :return: A list of remaining balances.
        :rtype: List[float]
        """
        remain_balances_list = [track.get_remaining_balances() for track in self.tracks]
        # Pad the lists with zeros and perform element-wise addition
        return [sum(x) for x in zip_longest(*remain_balances_list, fillvalue=0)]

    def get_annual_remain_balances(self) -> List[int]:
        """
        Get a list of annual remaining balances, where each element represents the sum of remaining balances across all tracks
        for a year time period.

        :return: A list of remaining balances.
        :rtype: List[float]
        """
        return [balance for i, balance in enumerate(self.get_remain_balances()) if i % 12 == 0]

    def get_total_payment(self, months_to_exit: Optional[int] = None) -> int:
        """
        Get the total payment, which is the sum of total payments across all mortgage tracks.

        :return: The total payment.
        :rtype: float
        """
        if months_to_exit is None:
            return sum([track.calculate_total_repayment() for track in self.tracks])
        return sum(self.get_monthly_payments()[:months_to_exit])

    def calculate_highest_monthly_payment(self) -> int:
        """
        Calculate the highest monthly payment across all monthly payments.

        :return: The highest monthly payment.
        :rtype: float
        """
        return max(self.get_monthly_payments())

    def calculate_initial_monthly_payment(self) -> int:
        """
        Calculate the initial monthly payment, which is the sum of initial monthly payments across all tracks.

        :return: The initial monthly payment.
        :rtype: float
        """
        return np.ceil(sum([track.calculate_initial_monthly_payment() for track in self.tracks]))

    def calculate_loan_yearly_irr(self):
        """
        Calculate the yearly internal rate of return (IRR) for the mortgage.
        Yearly IRR = Month IRR * 12 Months * 100 (Percentage) * -1 (Bank Investment)
        :return: The yearly IRR for the mortgage.
        :rtype: float (percentage)
        """
        monthly_cash_flow = [-self.total_initial_loan_amount] + self.get_monthly_payments()
        return npf.irr(monthly_cash_flow) * 12 * 100 * -1

    def get_num_of_payments(self) -> int:
        """
        Calculate the maximum number of payments among all mortgage tracks.

        :return: The maximum number of payments.
        :rtype: int
        """
        return max([track.num_payments for track in self.tracks])

    def print_payments(self):
        """

        :return:
        """
        plot_mortgage_monthly_payments(self.get_num_of_payments(),
                                       self.get_principal_payments(),
                                       self.get_interest_payments(),
                                       self.get_remain_balances())

    def total_loan_cost(self) -> float:
        """
        Calculate the total loan cost, considering the loan cost of each mortgage track and their respective percentages.

        :return: The total loan cost.
        :rtype: float
        """
        return sum([track.loan_cost() * percentage for track, percentage in self.get_tracks_percentages_dic().items()])

    def get_tracks_loan_cost(self) -> Dict[MortgageTrack, float]:
        """
        Calculate the loan cost for each mortgage track in the pipeline.

        :return: A dictionary where keys are MortgageTrack instances, and values represent the loan cost for each track.
        :rtype: Dict[MortgageTrack, float]
        """
        return {track: track.loan_cost() for track in self.tracks}

    def calculate_weighted_average_interest_rates(self) -> float:
        """
        Calculate the weighted average interest rate for the mortgage tracks in the pipeline.

        :return: The weighted average interest rate.
        :rtype: float
        """
        return sum([track.interest_rate * percentage for track, percentage in self.get_tracks_percentages_dic().items()])

    def plot_interest_and_principal_payments(self) -> None:
        """
        Plot the interest and principal payments over the loan term.

        Uses the utility function `plot_principal_and_interest_payments` to create the plot.

        :return: None
        """
        plot_principal_and_interest_payments(self.get_num_of_payments(), self.get_principal_payments(), self.get_interest_payments())

    def plot_monthly_payments(self) -> None:
        """
        Plot the monthly payments over the loan term.

        Uses the utility function `plot_monthly_payments` to create the plot.

        :return: None
        """
        plot_monthly_payments(self.get_num_of_payments(), self.get_monthly_payments())

    def plot_remain_balances(self) -> None:
        plot_remain_balances(self.get_remain_balances())

    def calculate_early_payment_fee(self, num_of_months: int, average_interest_in_early_payment: Dict[MortgageTrack.__class__, float]) -> int:
        """
        Calculate the early payment fee for the mortgage after a specified number of months.

        :param num_of_months: The number of months from the beginning of the loan.
        :type num_of_months: int

        :return: The early payment fee calculated based on the total fee for all mortgage tracks,
            considering the eligibility and discount factor.
        """
        #TODO : test this
        full_early_payment_fee = sum(track.calculate_early_payment_fee(num_of_months, average_interest_in_early_payment[track.__class__]) for track in self.tracks)
        eligibility_present = any(isinstance(track, Eligibility) for track in self.tracks)

        discount_factor = calculate_discount_factor(num_of_months, eligibility_present)
        return round(discount_factor * full_early_payment_fee)

    def calculate_normalize_resource_allocation(self) -> Dict[MortgageTrack, float]:
        """
        Calculate the normalized resource allocation for each mortgage track.

        Returns:
            Dict[Track, float]: A dictionary where keys are mortgage tracks, and values represent the normalized
            portion of the monthly payment allocated for the specific track. The normalization is calculated by
            dividing each track's initial monthly payment by the total initial monthly payment across all tracks.
        """
        return {track: track.calculate_initial_monthly_payment() / self.calculate_initial_monthly_payment() for track in self.tracks}

    def calculate_index_linkage_segmentation(self) -> Dict[LinkageType, float]:
        """
        Calculate the segmentation of mortgage tracks based on their linkage to an index.

        :return: A dictionary where keys are LinkageType enum values, and values represent the sum of percentages
            corresponding to tracks associated with each linkage type.
        :rtype: Dict[LinkageType, float]
        """
        #TODO
        return {LinkageType.Linked: sum([percentage for track, percentage in self.get_tracks_percentages_dic().items() if track in LinkageType.Linked.value]),
                LinkageType.NotLinked: sum([percentage for track, percentage in self.get_tracks_percentages_dic().items() if track in LinkageType.NotLinked.value]),
                LinkageType.Prime: sum([percentage for track, percentage in self.get_tracks_percentages_dic().items() if track in LinkageType.Prime.value])}


    def calculate_interest_type_segmentation(self) -> Dict[InterestType, float]:
        """
        Calculate the segmentation of mortgage tracks based on their interest type.

        :return: A dictionary where keys are InterestType enum values, and values represent the sum of percentages
            corresponding to tracks associated with each interest type.
        :rtype: Dict[InterestType, float]
        """

        # sum_i = 0
        # for track, percentage in self.get_tracks_percentages_dic().items():
        #     for my_class in  InterestType.Constant.value:
        #         from src.mortgage_tracks.constant_not_linked import ConstantNotLinked
        #         from src.mortgage_tracks.constant_not_linked import ConstantNotLinked
        #         if isinstance(track, my_class):
        #             sum_i +=  percentage
        # TODO
        return {InterestType.Constant: sum([percentage for track, percentage in self.get_tracks_percentages_dic().items() if any(isinstance(track, class_type) for class_type in InterestType.Constant.value)]),
                InterestType.NotConstant: sum([percentage for track, percentage in self.get_tracks_percentages_dic().items() if any(isinstance(track, class_type) for class_type in InterestType.NotConstant.value)]),
                InterestType.Prime: sum([percentage for track, percentage in self.get_tracks_percentages_dic().items() if track in any(isinstance(track, class_type) for class_type in InterestType.Prime.value)])}


    def calculate_total_cost_of_borrowing(self, years_to_exit: Optional[int] = None, average_interest_in_early_payment: Optional[Dict[MortgageTrack, float]] = None) -> int:
        """
        Calculate the total cost of borrowing over the investment period.

        :param years_to_exit: Optional. Number of years until exit. If not provided, calculates the total cost of borrowing until the end of the loan term.
        :param average_interest_in_early_payment: Optional. Dictionary mapping MortgageTrack instances to their average interest rates during early payments.
        :return: The calculated total cost of borrowing.
        """
        if years_to_exit is None or average_interest_in_early_payment is None:
            return round(self.get_total_payment() - self.total_initial_loan_amount)
        else:
            months_to_exit = 12 * years_to_exit
            return round(sum(self.get_interest_payments()[:months_to_exit]) + self.calculate_early_payment_fee(months_to_exit, average_interest_in_early_payment))


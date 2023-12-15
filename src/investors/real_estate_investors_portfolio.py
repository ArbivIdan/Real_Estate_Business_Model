from src.investors.real_estate_investor import RealEstateInvestor
from src.mortgage.mortgage_utils.mortgage_financial_utils_il import calculate_maximum_loan_amount
from src.investors.Israel.real_estate_investment_type import RealEstateInvestmentType
from typing import Optional
import matplotlib.pyplot as plt

class RealEstateInvestorsPortfolio:
    def __init__(self, *real_estate_investor: RealEstateInvestor):

        self.investors = list(real_estate_investor)
        self.num_borrowers = (len(self.investors))

    def calculate_total_disposable_income(self) -> int:
        """
        Calculate the total disposable income across all investors in the portfolio.

        :return: The calculated total disposable income.
        :rtype: int
        """
        return sum([investor.disposable_income for investor in self.investors])

    def calculate_monthly_total_debt_payment(self) -> int:
        """
        Calculate the total monthly debt payments across all investors in the portfolio.

        :return: The calculated total monthly debt payments.
        :rtype: int
        """
        return sum([investor.total_debt_payment for investor in self.investors])

    def calculate_annual_total_debt_payment(self) -> int:
        """
        Calculate the total annual debt payments across all investors in the portfolio.

        :return: The calculated total annual debt payments.
        :rtype: int
        """
        return 12 * self.calculate_monthly_total_debt_payment()

    def calculate_monthly_total_net_income(self) -> int:
        """
        Calculate the total monthly net income across all investors in the portfolio.

        :return: The calculated total monthly net income.
        :rtype: int
        """
        return sum([investor.net_monthly_income for investor in self.investors])

    def calculate_annual_total_net_income(self) -> int:
        """
        Calculate the total annual net income across all investors in the portfolio.

        :return: The calculated total annual net income.
        :rtype: int
        """
        return 12 * self.calculate_monthly_total_net_income()

    def calculate_maximum_monthly_loan_repayment(self) -> int:
        """
        Calculate the total maximum monthly loan repayment across all investors in the portfolio.

        :return: The calculated total maximum monthly loan repayment.
        :rtype: int
        """
        return sum([investor.calculate_maximum_monthly_loan_repayment() for investor in self.investors])

    def calculate_total_available_equity(self) -> int:
        """
        Calculate the total available equity across all investors in the portfolio.

        :return: The calculated total available equity.
        :rtype: int
        """
        return sum([investor.total_available_equity for investor in self.investors])

    def calculate_maximum_loan_amount(self, monthly_payment: Optional[int] = None, num_payments: int = 360) -> int:
        """
        Calculate the maximum loan amount based on the specified or maximum monthly loan repayment.

        :param specified_monthly_payment: The specified monthly loan repayment amount.
        :type specified_monthly_payment: int, optional
        :param num_payments: The total number of loan payments (default is 360).
        :type num_payments: int
        :return: The calculated maximum loan amount.
        :rtype: int
        """
        if monthly_payment is None:
            monthly_payment = self.calculate_maximum_monthly_loan_repayment()
        maximum_monthly_loan_repayment = self.calculate_maximum_monthly_loan_repayment()
        if monthly_payment > maximum_monthly_loan_repayment:
            assert False, f"Monthly payment '{monthly_payment}' exceeds the maximum allowable monthly loan repayment '{maximum_monthly_loan_repayment}'."
        return calculate_maximum_loan_amount(num_payments, monthly_payment)

    def get_investors_purchase_taxes_type(self) -> RealEstateInvestmentType:
        """
        Get the real estate investment type for purchase taxes calculation.

        :return: The real estate investment type for purchase taxes.
        :rtype: RealEstateInvestmentType
        """
        return RealEstateInvestmentType.SingleApartment

    def get_investors_selling_taxes_type(self) -> RealEstateInvestmentType:
        """
        Get the real estate investment type for selling taxes calculation.

        :return: The real estate investment type for selling taxes.
        :rtype: RealEstateInvestmentType
        """
        return RealEstateInvestmentType.SingleApartment

    def get_gross_rental_income(self) -> int:
        """
        Calculate the total gross rental income across all investors in the portfolio.

        :return: The calculated total gross rental income.
        :rtype: int
        """
        return sum([investor.gross_rental_income for investor in self.investors])

    def calculate_maximum_property_price(self) -> int:
        """
        Calculate the maximum property price that can be purchased by investors in the portfolio.

        :return: The calculated maximum property price.
        :rtype: int
        """
        # TODO: check how multiple ppl take loans works
        max_possible_ltv = min([investor.real_estate_investment_type.value for investor in self.investors])
        total_available_equity = self.calculate_total_available_equity()
        maximum_property_price = total_available_equity / (1 - max_possible_ltv)
        loan_needed = maximum_property_price - total_available_equity
        if loan_needed > self.calculate_maximum_loan_amount():
            maximum_property_price = total_available_equity + self.calculate_maximum_loan_amount()
        return maximum_property_price

    def plot_maximum_property_price_vs_total_available_equity(self) -> None:
        max_possible_ltv = min([investor.real_estate_investment_type.value for investor in self.investors])
        total_available_equity = self.calculate_total_available_equity()
        total_available_equities =  [total_available_equity + i * 100_000 for i in range(-4, 5)]
        y_s =[self.calculate_max_price(max_possible_ltv, equity) for equity in total_available_equities]

        plt.plot(total_available_equities, y_s)
        plt.xlabel('Equity Available')
        plt.ylabel('Maximum Purchase Price')
        plt.title('Maximum Purchase Price vs Equity Available')

        for x, y in zip(total_available_equities, y_s):
            plt.text(x, y, f'({x/1_000_000:.2f}M, {y/1_000_000:.2f}M)', ha='left', va='bottom')

        plt.legend()
        plt.show()

    def calculate_max_price(self, max_possible_ltv, total_available_equity):
        maximum_property_price = total_available_equity / (1 - max_possible_ltv)
        loan_needed = maximum_property_price - total_available_equity
        if loan_needed > self.calculate_maximum_loan_amount():
            maximum_property_price = total_available_equity + self.calculate_maximum_loan_amount()
        return maximum_property_price




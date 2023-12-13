from mortgage_tracks.change_not_linked import ChangeNotLinked
from mortgage_tracks.constant_linked import ConstantLinked
from mortgage_tracks.constant_not_linked import ConstantNotLinked
from mortgage_tracks.prime import Prime
from src.investors.real_estate_investment_type import RealEstateInvestmentType
from src.investors.real_estate_investor import RealEstateInvestor
from src.investors.real_estate_investors_portfolio import RealEstateInvestorsPortfolio
from src.mortgage_pipeline import MortgagePipeline

def main():
    # Example values
    loan_amount = 100_000
    initial_interest_rate = 4 / 100
    num_payments = 360

    # Constant Not Linked
    constant_not_linked = ConstantNotLinked(5/100, 120, loan_amount, [0 for _ in range(num_payments)], [0 for _ in range(num_payments)])

    # Constant Linked
    consumer_price_index = [0.02 / 12 for _ in range(num_payments)]
    constant_linked = ConstantLinked(initial_interest_rate, num_payments, loan_amount, consumer_price_index, [0 for _ in range(num_payments)])

    # Prime
    bank_of_israel_interest_rate = [4 for _ in range(num_payments)]
    percentage_changes = [(b - a) / a * 100 for a, b in zip(bank_of_israel_interest_rate[:-1], bank_of_israel_interest_rate[1:])]
    percentage_changes.insert(0, 0)
    prime_interest = "p-0.5"
    prime_interest = eval(prime_interest[1:])
    prime = Prime((bank_of_israel_interest_rate[0] + 1.5 + prime_interest) / 100, num_payments, loan_amount, percentage_changes, [0 for _ in range(num_payments)])

    # Change every 5 years not linked
    change_every_5_not_linked = ChangeNotLinked(initial_interest_rate, num_payments, loan_amount, [0 for _ in range(num_payments)], [0 for _ in range(num_payments)], 60)
    # Change every 5 years, Linked


    mortgage = MortgagePipeline(constant_linked, constant_not_linked)
    mortgage.plot_monthly_payments()
    mortgage.plot_interest_and_principal_payments()



    # idan_arbiv = RealEstateInvestor(25000, 2_000, RealEstateInvestmentType.SingleApartment, 700000)
    # investment_portfolio = RealEstateInvestorsPortfolio(idan_arbiv)
    # print(f"Idan's maximum monthly payment is: {investment_portfolio.calculate_maximum_monthly_loan_repayment()} NIS")
    # maximum_loan_amount = round((investment_portfolio.calculate_maximum_loan_amount() / 1_000_000), 2)
    # print(f"Idan's maximum loan amount is: {maximum_loan_amount}M")
    # print(f"The maximum property value that idan can buy is {round(investment_portfolio.calculate_maximum_property_price() / 1_000_000, 2)} million ")



if __name__ == "__main__":
    main()

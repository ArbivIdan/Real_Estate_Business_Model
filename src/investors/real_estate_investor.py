from src.investors.Israel.real_estate_investment_type import RealEstateInvestmentType
from typing import Optional

from src.investors.investors_constants import InvestorsConstants


class RealEstateInvestor:
    def __init__(self, net_monthly_income: int, total_debt_payment: int,
                 real_estate_investment_type: RealEstateInvestmentType, total_available_equity: int,
                 gross_rental_income: Optional[int] = 0):
        """
        ההכנסות המוכרות על ידי הבנקים:

            משכורת חודשית
            מלגה או קצבת נכות (בחלק מהבנקים)
            הכנסה מעסק
            דיבידנדים של שכיר בעל שליטה מעסק שבבעלותו המלאה
            הכנסה משכר דירה שבבעלותך בטאבו.

        ומה מבחינתם לא נחשב כהכנסה?
            1. דיבידנדים ממניות, RSU.
            2. כל הכנסה (למעט אלו שצוינו לעיל) שלא מתקבלת מדי חודש בחודשו.
            3. הכנסה מדירה שאינה בבעלותך.



        ההחזרים החודשיים בגין כל ההתחייבות שיורדות מהחשבון שלך מדי חודש בחודשו ויתרת התשלומים שנותרו גדולה מ18 חודשים.


        :param monthly_income:
        :param active_loans_amount:
        """
        self.net_monthly_income = net_monthly_income
        self.total_debt_payment = total_debt_payment
        self.real_estate_investment_type = real_estate_investment_type
        self.disposable_income = net_monthly_income - total_debt_payment
        self.total_available_equity = total_available_equity
        self.gross_rental_income = gross_rental_income

    def calculate_maximum_monthly_loan_repayment(self, constructor_linked_amount_percentage: Optional[float] = None) -> int:
        """
        Calculate the maximum monthly loan repayment based on disposable income and constructor-linked amount percentage.

        :param constructor_linked_amount_percentage: The percentage of disposable income linked to the constructor, defaults to InvestorsConstants.CONSTRUCTOR_LINKED_AMOUNT_PERCENTAGE.
        :type constructor_linked_amount_percentage: Optional[float]
        :return: The calculated maximum monthly loan repayment.
        :rtype: int
        """
        if constructor_linked_amount_percentage is None:
            constructor_linked_amount_percentage = InvestorsConstants.CONSTRUCTOR_LINKED_AMOUNT_PERCENTAGE
        return round(constructor_linked_amount_percentage * self.disposable_income)

    def calculate_max_property_price_for_investor(self) -> int:
        """
        Calculate the maximum property price that investor can purchase based on the maximum monthly loan repayment and real estate investment type.

        :return: The calculated maximum property price.
        :rtype: int
        """
        return self.calculate_maximum_monthly_loan_repayment() * self.real_estate_investment_type.value

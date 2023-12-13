from src.investors.real_estate_investment_type import RealEstateInvestmentType
from typing import Optional


class RealEstateInvestor:
    def __init__(self, net_monthly_income: int, total_debt_payment: int, real_estate_investment_type: RealEstateInvestmentType, total_available_equity: int, gross_rental_income: Optional[int] = 0):
        self.net_monthly_income = net_monthly_income
        self.total_debt_payment = total_debt_payment
        self.real_estate_invest_type = real_estate_investment_type
        self.disposable_income = net_monthly_income - total_debt_payment
        self.total_available_equity = total_available_equity
        self.maximum_monthly_loan_repayment = 0.4 * self.disposable_income
        self.maximum_property_price = self.maximum_monthly_loan_repayment * real_estate_investment_type.value
        self.gross_rental_income = gross_rental_income
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
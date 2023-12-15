import numpy_financial as npf
import numpy as np
from typing import List, Union


def calculate_early_payment_fee(A: float, B: List[Union[int, float]], C: float, R: float, n: int) -> int:
    """
    for more info refer - https://www.boi.org.il/media/qy5cow0l/116.pdf
    :param A: הריבית הממוצעת התקופתית ביום הפירעון המוקדם, כהגדרתה בסעיף 1 לצו זה
    :param B: התשלומים העתידיים התקופתיים בהתאם לתנאי ההלוואה לרבות ריבית שתצטבר
    :param C: הריבית הממוצעת התקופתית במועד העמדת ההלוואה, כהגדרתה בסעיף 1 לצו זה
    :param R: הריבית התקופתית החלה על ההלוואה ביום הפירעון המוקדם
    :param n: מספר תקופות מיום הפירעון המוקדם עד יום שינוי הריבית
    :return: early payment fee
    """
    A, C, R = A / 12, C / 12, R / 12
    # in this case only aa + cc
    if n < 0 or n > len(B):
        n = len(B)
    B_n = B[:n]
    B_N = B[n:]
    C = min(C, R)
    aa = npf.npv(A, [0.0] + B_n)
    bb = (1 / np.power(1 + A, n)) * npf.npv(R, [0.0] + B_N)
    cc = npf.npv(C, [0.0] + B_n)
    dd = (1 / np.power(1 + C, n)) * npf.npv(R, [0.0] + B_N)
    # print(cc + dd)
    return round(aa + bb - (cc + dd))
    # return aa + bb - (cc + dd)


def calculate_discount_factor(num_of_months: int, eligibility_present: bool) -> float:
    """
    for more info refer: https://www.mashkanta4.me/%d7%9e%d7%a8%d7%9b%d7%96-%d7%94%d7%99%d7%93%d7%a2/prepayment_fee/
    :param num_of_months:
    :param eligibility_present:
    :return:
    """
    if eligibility_present:
        if num_of_months >= 48:
            return 0.6
        elif num_of_months >= 36:
            return 0.7
        elif num_of_months >= 24:
            return 0.8
        elif num_of_months >= 12:
            return 0.9
    else:
        if num_of_months >= 60:
            return 0.7
        elif num_of_months >= 36:
            return 0.8
    return 1.0


def calculate_maximum_loan_amount(num_payments: int, monthly_payment: int) -> int:
    # Given values
    # TODO: Need to check how this interest selected, and need to fetch the avg interest to fill this parameter
    interest_rate = 0.05  # 5%

    # Calculate the present value (loan amount)
    return npf.pv(interest_rate / 12, num_payments, -monthly_payment)




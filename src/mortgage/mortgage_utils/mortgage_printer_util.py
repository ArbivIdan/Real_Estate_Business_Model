
def plot_mortgage_monthly_payments(num_payments, principal_payments, interest_payments, remaining_balances):
    for period, principal_payment, interest_payment, remaining_balance in zip(range(1, num_payments + 1),
                                                                              principal_payments,
                                                                              interest_payments,
                                                                              remaining_balances):
        print(f"Period {period}: Principal Payment=${principal_payment}, "
              f"Interest Payment=${interest_payment}, Monthly Payment=${round(interest_payment + principal_payment)},"
              f" Remaining Balance=${round(remaining_balance)}")

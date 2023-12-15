import matplotlib.pyplot as plt
from typing import List


def plot_monthly_payments(max_num_of_payments: int, monthly_payments: List[float]):
    x_values = list(range(1, max_num_of_payments + 1))
    plt.plot(x_values, monthly_payments, label='Monthly Payments')
    plt.xlabel('Payment Number')
    plt.ylabel('Payment Amount')
    plt.title('Loan Payments Over Time')
    plt.legend()
    plt.show()

def plot_principal_and_interest_payments(max_num_of_payments: int, principal_payments: List[float], interest_payments: List[float]):
    x_values = list(range(1, max_num_of_payments + 1))
    plt.plot(x_values, principal_payments, label='Principal Payments')
    plt.plot(x_values, interest_payments, label='Interest Payments')
    plt.xlabel('Payment Number (Month)')
    plt.ylabel('Payment Amount (NIS)')
    plt.title('Loan Payments Over Time')
    plt.legend()
    plt.show()


def plot_remain_balances(remain_balances: List[int]):
    plt.plot(remain_balances, label='Remain Balances')
    plt.xlabel('Payment Number (Month)')
    plt.ylabel('Payment Amount (NIS)')
    plt.title('Loan Payments Over Time')
    plt.legend()
    plt.show()
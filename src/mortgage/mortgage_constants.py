import numpy as np


# TODO: should be converted to external configuration file

class MortgageConstants:
    MONTHS_IN_YEAR = 12
    FINWIZ_CHANGE_LINKED_EVERY_FIVE = [1.66, 2.1, 2.29, 2.35, 2.37, 2.37]
    INDICES_FOR_CHANGE_LINKED_EVERY_FIVE = np.arange(360) % 60 == 0
    FINWIZ_CHANGE_LINKED_EVERY_FIVE_CHANGING = [0.0] + [b - a for a, b in zip(FINWIZ_CHANGE_LINKED_EVERY_FIVE[:-1],
                                                                              FINWIZ_CHANGE_LINKED_EVERY_FIVE[1:])]
    INTEREST_CHANGE_FOR_CHANGE_LINKED_EVERY_FIVE = np.zeros(360)
    INTEREST_CHANGE_FOR_CHANGE_LINKED_EVERY_FIVE[
        INDICES_FOR_CHANGE_LINKED_EVERY_FIVE] = FINWIZ_CHANGE_LINKED_EVERY_FIVE_CHANGING


if __name__ == "__main__":
    print(MortgageConstants.INTEREST_CHANGE_FOR_CHANGE_LINKED_EVERY_FIVE)

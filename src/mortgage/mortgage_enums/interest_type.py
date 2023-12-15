from enum import Enum
from src.mortgage.mortgage_tracks.change_linked import ChangeLinked
from src.mortgage.mortgage_tracks.change_not_linked import ChangeNotLinked
from src.mortgage.mortgage_tracks.constant_linked import ConstantLinked
from src.mortgage.mortgage_tracks.constant_not_linked import ConstantNotLinked
from src.mortgage.mortgage_tracks.eligibility import Eligibility
from src.mortgage.mortgage_tracks.prime import Prime


class InterestType(Enum):
    """
    Enumeration representing different types of interest rates.

    - Constant: Interest rates that remain constant throughout the loan term.
      - ConstantLinked: Constant interest rate linked to an index.
      - ConstantNotLinked: Constant interest rate not linked to an index.

    - NotConstant: Interest rates that can change over the loan term.
      - Eligibility: Interest rate based on eligibility criteria.
      - ChangeLinked: Changing interest rate linked to an index.
      - ChangeNotLinked: Changing interest rate not linked to an index.

    - Prime: Interest rates linked to the prime rate.
    """
    Constant = {ConstantLinked, ConstantNotLinked}
    NotConstant = {Eligibility, ChangeLinked, ChangeNotLinked}
    Prime = {Prime}



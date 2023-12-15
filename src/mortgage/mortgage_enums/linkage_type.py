from enum import Enum
from src.mortgage.mortgage_tracks.change_linked import ChangeLinked
from src.mortgage.mortgage_tracks.change_not_linked import ChangeNotLinked
from src.mortgage.mortgage_tracks.constant_linked import ConstantLinked
from src.mortgage.mortgage_tracks.constant_not_linked import ConstantNotLinked
from src.mortgage.mortgage_tracks.eligibility import Eligibility
from src.mortgage.mortgage_tracks.prime import Prime


class LinkageType(Enum):
    """
    Enumeration representing different types of loan interest linkage.

    - Linked: Loans with interest rates linked to an index or eligibility.
      - ChangeLinked: Changing interest rate linked to an index.
      - ConstantLinked: Constant interest rate linked to an index.
      - Eligibility: Interest rate based on eligibility criteria.

    - NotLinked: Loans with interest rates not linked to an index.
      - ChangeNotLinked: Changing interest rate not linked to an index.
      - ConstantNotLinked: Constant interest rate not linked to an index.

    - Prime: Loans with interest rates linked to the prime rate.
    """
    Linked = {ChangeLinked, ConstantLinked, Eligibility}
    NotLinked = {ChangeNotLinked, ConstantNotLinked}
    Prime = {Prime}

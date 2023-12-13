from enum import Enum
from src.mortgage_tracks.change_linked import ChangeLinked
from src.mortgage_tracks.change_not_linked import ChangeNotLinked
from src.mortgage_tracks.constant_linked import ConstantLinked
from src.mortgage_tracks.constant_not_linked import ConstantNotLinked
from src.mortgage_tracks.eligibility import Eligibility
from src.mortgage_tracks.prime import Prime


class LinkageType(Enum):
    Linked = {ChangeLinked, ConstantLinked, Eligibility}
    NotLinked = {ChangeNotLinked, ConstantNotLinked}
    Prime = {Prime}

from enum import Enum


class RealEstateInvestmentType(Enum):
    """
    The values represent the maximum financing percentage given to the type of borrower
    """
    SingleApartment = 0.75
    AlternativeApartment = 0.7
    AdditionalApartment = 0.5
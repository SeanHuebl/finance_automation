from enum import Enum

class TransactionType(Enum):
    """
    Enum representing the type of a financial transaction.

    Attributes:
        DEBIT (str): Indicates a debit transaction.
        CREDIT (str): Indicates a credit transaction.
    """
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'

class PaidOff(Enum):
    """
    Enum representing paid-off transactions that should be excluded.

    Attributes:
        FIDELITY_PAYMENT (str): Indicates a paid-off Fidelity transaction.
        COSTCO_PAYMENT (str): Indicates a paid-off Costco transaction.
    """
    FIDELITY_PAYMENT = 'INTERNET PAYMENT THANK'
    COSTCO_PAYMENT = 'ONLINE PAYMENT, THANK YOU'

class TransactionName(Enum):
    """
    Enum representing specific transaction names for categorization.

    This enum lists various names that are used to identify and standardize transactions 
    based on predefined patterns.

    Attributes:
        PAYPAL (str): Represents PayPal transactions.
        CPI (str): Represents CPI transactions.
        VC (str): Represents VC transactions.
        SQ (str): Represents SQ transactions.
        VENDING_MACHINE (str): Represents Vending Machine transactions.
        VET (str): Represents Veterinary-related transactions.
        STARBUCKSSE (str): Represents a shorthand for Starbucks transactions.
        STARBUCKS (str): Represents standard Starbucks transactions.
        AMAZON_PRIME (str): Represents Amazon Prime transactions.
        AMAZON (tuple): Represents standard Amazon transactions.
        COSTCO (str): Represents Costco transactions.
        A_CLIP_ABOVE (str): Represents the groomer service 'A Clip Above'.
        GROOMER (str): Represents generic grooming services.
        WAX (str): Represents European Wax Center transactions.
        LIBERTY_MUTUAL (str): Represents Liberty Mutual transactions.
        RENTERS_INSURANCE (str): Represents Renter's Insurance payments.
        CAR_INSURANCE (str): Represents Car Insurance payments.
        ENT_CU (str): Represents ENT Credit Union transactions.
        CAR_PAYMENT (str): Represents Car Payment transactions.
        PL (str): Represents shorthand for property lease payments.
        RENT (str): Represents Rent payments.
        DHHA (str): Represents Denver Health and Hospital Authority transactions.
        DENVER_HEALTH (str): Represents Denver Health transactions.
        AH (str): Represents Advent Health-related transactions.
        ADVENT (str): Represents standard Advent Health transactions.
        INTEREST_EARNED (str): Represents transactions for earned interest.
        INTEREST (str): Represents standardized interest transactions.
        HEALTH_ONE (str): Represents HealthOne medical transactions.
        SWEDISH (str): Represents Swedish Medical Center transactions.
        DIRECT_DEPOSIT (str): Represents direct deposit transactions.
    """
    PAYPAL = 'PAYPAL '
    CPI = 'CPI'
    VC = 'VC'
    SQ = 'SQ '
    VENDING_MACHINE = 'VENDING MACHINE'
    VET = 'VET'
    STARBUCKSSE = 'STARBUCKSSE'
    STARBUCKS = 'STARBUCKS'
    AMAZON_PRIME = 'Amazon Prime'
    AMAZON = ('AMAZON', 'AMZN')
    COSTCO = 'COSTCO'
    A_CLIP_ABOVE = 'A CLIP ABOVE'
    GROOMER = 'GROOMER'
    WAX = 'EUROPEAN WAX CENTER'
    LIBERTY_MUTUAL = 'LIBERTY MUTUAL'
    RENTERS_INSURANCE = 'RENTERS INSURANCE'
    CAR_INSURANCE = 'CAR INSURANCE'
    ENT_CU = 'ENT CU'
    CAR_PAYMENT = 'CAR PAYMENT'
    PL = 'PL'
    RENT = 'RENT'
    DHHA = 'DENVER HEALTH AN'
    DENVER_HEALTH = 'DENVER HEALTH'
    AH = 'AH ROCKY MOUNTAI'
    ADVENT = 'ADVENT HEALTH'
    INTEREST_EARNED = 'INTEREST EARNED'
    INTEREST = 'INTEREST'
    HEALTH_ONE = 'HEALTHONE'
    SWEDISH = 'HEALTH ONE'
    DIRECT_DEPOSIT = 'Direct Deposit'

class Category(Enum):
    """
    Enum representing various transaction categories.

    This enum is used to classify transactions into different categories for easier analysis.

    Attributes:
        INCOME (str): Represents income-related transactions.
        UTILITIES (str): Represents utility-related transactions.
        FOOD (str): Represents food-related transactions.
        CAR (str): Represents car-related expenses.
        HOUSING (str): Represents housing-related expenses.
        SUBSCRIPTIONS (str): Represents subscription services.
        MEDICAL (str): Represents medical-related transactions.
        PET (str): Represents pet-related expenses.
        OTHER (str): Represents other types of transactions not covered by other categories.
    """
    INCOME = 'INCOME'
    UTILITIES = 'UTILITIES'
    FOOD = 'FOOD'
    CAR = 'CAR'
    HOUSING = 'HOUSING'
    SUBSCRIPTIONS = 'SUBSCRIPTIONS'
    MEDICAL = 'MEDICAL'
    PET = 'PET'
    OTHER = 'OTHER'
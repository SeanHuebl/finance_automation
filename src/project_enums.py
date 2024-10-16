from enum import Enum

# Transaction types

class TransactionType(Enum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'

class PaidOff(Enum):
    FIDELITY_PAYMENT = 'INTERNET PAYMENT THANK'
    COSTCO_PAYMENT = 'ONLINE PAYMENT, THANK YOU'

class TransactionName(Enum):
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

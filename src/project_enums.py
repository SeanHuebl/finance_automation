from enum import Enum

# Transaction types

class TransactionType(Enum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'

class PaidOff(Enum):
    PAYMENT = 'INTERNET PAYMENT THANK'
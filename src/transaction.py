from project_enums import TransactionType

class Transaction():
    def __init__(self, date: str, name: str, amount: float) -> None:
        self.date = date
        self.name = name
        self.amount = amount
    
    def __repr__(self) -> str:
        return f'Date: {self.date} | Name: {self.name} | Amount: {self.amount}'
    
class Debit(Transaction):
    def __init__(self, date: str, name: str, amount: float) -> None:
        super().__init__(date, name, amount)
        self.type = TransactionType.DEBIT

    def __repr__(self) -> str:
        return f'Type: {self.type.value} | Date: {self.date} | Name: {self.name} | Amount: {self.amount}'
    
class Credit(Transaction):
    def __init__(self, date: str, name: str, amount: float) -> None:
        super().__init__(date, name, amount)
        self.type = TransactionType.CREDIT

    def __repr__(self) -> str:
        return f'Type: {self.type.value} | Date: {self.date} | Name: {self.name} | Amount: {self.amount}'
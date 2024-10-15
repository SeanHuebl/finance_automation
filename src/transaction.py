
class Transaction():
    def __init__(self, date: str, name: str, amount: float) -> None:
        self.date = date
        self.name = name
        self.amount = amount
    
    def __repr__(self) -> str:
        return f'Date: {self.date} | Name: {self.name} | Amount: {self.amount}'
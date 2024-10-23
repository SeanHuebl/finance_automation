import os
import pandas as pd
import re

from project_enums import PaidOff, TransactionName, TransactionType

def clean_data_fidelity(csv_path: str) -> pd.DataFrame:
    if not csv_path or not isinstance(csv_path, str):
        raise ValueError('Arg: csv_path must exist and be of type str')
    if not os.path.exists:
        raise ValueError('Arg: csv_path must be a valid file path')
    if not csv_path.endswith('.csv'):
        raise ValueError('Arg csv_path must be of file type .csv')

    df: pd.DataFrame = clean_csv(csv_path)
    df['Name'] = df['Name'].str[:22]
    df = df[df['Name'] != PaidOff.FIDELITY_PAYMENT.value]
    df['Date'] = df.apply(fix_date, axis=1)
    df['Amount'] = df.apply(fix_amount, axis=1)
    df['Name'] = df.apply(clean_transaction_name, axis=1)
    return df


def clean_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return df.drop('Memo', axis=1)

def fix_date(row: pd.DataFrame) -> str:
    date: pd.Timestamp = pd.to_datetime(row['Date'], format='%Y-%m-%d')
    date = date.strftime('%m/%d/%Y')
    return date
    
def fix_amount(row: pd.DataFrame) -> float:
    if row['Transaction'] == TransactionType.DEBIT.value:
        return row['Amount'] * -1
    return row['Amount']
    
def clean_transaction_name(row: pd.DataFrame) -> str:
    name: str = row['Name']
    result = re.split(r'[*#\d\.-]', name)
    
    match result[0]:
        case TransactionName.PAYPAL.value:
            name = result[1].rstrip()
            if name == TransactionName.STARBUCKSSE.value:
                name = TransactionName.STARBUCKS.value
        case TransactionName.CPI.value:
            name = TransactionName.VENDING_MACHINE.value
        case TransactionName.VC.value:
            name = TransactionName.VET.value
        case TransactionName.SQ.value:
            name = result[1].rstrip()
            if name == TransactionName.A_CLIP_ABOVE.value:
                name = TransactionName.GROOMER.value
        case TransactionName.AMAZON_PRIME.value:
            name = TransactionName.AMAZON_PRIME.value.upper()
        case _:
            name = result[0].rstrip().upper()

            for _ in TransactionName.AMAZON.value:
                if _ in name:
                    name = TransactionName.AMAZON.value[0]

            if TransactionName.COSTCO.value in name:
                name = TransactionName.COSTCO.value
            
    return name
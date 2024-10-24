import os
import pandas as pd
import re

from project_enums import PaidOff, TransactionName

def clean_data_costco(csv_path: str) -> pd.DataFrame:
    if not csv_path or not isinstance(csv_path, str):
        raise ValueError('Arg: csv_path must exist and be of type str')
    if not os.path.exists:
        raise ValueError('Arg: csv_path must be a valid file path')
    if not csv_path.endswith('.csv'):
        raise ValueError('Arg csv_path must be of file type .csv')

    df: pd.DataFrame = _clean_csv(csv_path)
    df = df[df['Name'] != PaidOff.COSTCO_PAYMENT.value]
    df['Name'] = df.apply(_clean_transaction_name, axis=1)
    return df

def _clean_csv(csv_path: str) -> pd.DataFrame:
    if not csv_path or not isinstance(csv_path, str):
        raise ValueError('Arg: csv_path must exist and be of type str')
    if not os.path.exists:
        raise ValueError('Arg: csv_path must be a valid file path')
    if not csv_path.endswith('.csv'):
        raise ValueError('Arg csv_path must be of file type .csv')
    
    df: pd.DataFrame = pd.read_csv(csv_path)
    df = df.drop(['Status', 'Member Name'], axis=1)
    df['Transaction'] = ['DEBIT' if not pd.isna(a) else 'CREDIT' for a in df['Debit']]
    col = df.pop('Transaction')
    df.insert(1, 'Transaction', col)
    df = df.rename(columns={'Description': 'Name'})
    df['Amount'] = [a if not pd.isna(a) else b * -1 for a, b in zip(df['Debit'], df['Credit'])]
    df = df.drop(['Debit', 'Credit'], axis=1)
    return df

def _clean_transaction_name(row: pd.DataFrame) -> str:
    if row.empty or not isinstance(row, pd.DataFrame):
        raise ValueError('Arg: row must not be empty and must be of class pd.DataFrame')
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
            if TransactionName.WAX.value in name:
                    name = TransactionName.WAX.value
    return name
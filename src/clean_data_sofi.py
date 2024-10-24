import os
import pandas as pd
import re

from project_enums import TransactionName, TransactionType
from typing import List

def clean_data_sofi(csv_path: str) -> pd.DataFrame:
    if not csv_path or not isinstance(csv_path, str):
        raise ValueError('Arg: csv_path must exist and be of type str')
    if not os.path.exists:
        raise ValueError('Arg: csv_path must be a valid file path')
    if not csv_path.endswith('.csv'):
        raise ValueError('Arg csv_path must be of file type .csv')
    
    df: pd.DataFrame = _clean_csv(csv_path)
    df[['Transaction', 'Name', 'Amount']] = df.apply(_clean_name, axis=1).apply(pd.Series)
    return df

def _clean_csv(csv_path: str) -> pd.DataFrame:
    if not csv_path or not isinstance(csv_path, str):
        raise ValueError('Arg: csv_path must exist and be of type str')
    if not os.path.exists:
        raise ValueError('Arg: csv_path must be a valid file path')
    if not csv_path.endswith('.csv'):
        raise ValueError('Arg csv_path must be of file type .csv')
    
    df: pd.DataFrame = pd.read_csv(csv_path)
    df.drop(['Current balance', 'Status'], axis=1, inplace=True)
    df = df[
        (df['Description'] != 'CARDMEMBER SERV') & 
        (df['Description'] != 'FID BKG SVC LLC') & 
        (df['Description'] != 'CITI CARD ONLINE') &
        (df['Type'] != 'Deposit') & 
        (df['Type'] != 'Withdrawal')
        ].copy()
    df.rename(columns={'Description' : 'Name'}, inplace=True)
    df.insert(1, 'Transaction', df.pop('Type'))
    df['Amount'] = df['Amount'].mask(df['Amount'] < 0, df['Amount'] * -1, axis=0)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    return df

def _clean_name(row: pd.DataFrame) -> tuple[str, str, float]:
    if row.empty or not isinstance(row, pd.DataFrame):
        raise ValueError('Arg: row must not be empty and must be of class pd.DataFrame')
    transaction: str = row['Transaction']
    name: str = row['Name']
    amount: float = row['Amount']
    
    name = name.upper()
    if transaction == TransactionName.DIRECT_DEPOSIT.value or transaction.upper() == TransactionName.INTEREST_EARNED.value:
        transaction = TransactionType.CREDIT.value
    else:
        transaction = TransactionType.DEBIT.value
        
    result: List[str]= re.split(r'[*#\d\.-]', name)

    match result[0]:
        case TransactionName.LIBERTY_MUTUAL.value:
            if amount < 25.00:
                name = TransactionName.RENTERS_INSURANCE.value
            else:
                name = TransactionName.CAR_INSURANCE.value

        case TransactionName.ENT_CU.value:
            name = TransactionName.CAR_PAYMENT.value
        
        case TransactionName.PL.value:
            name = TransactionName.RENT.value
        
        case TransactionName.DHHA.value:
            name = TransactionName.DENVER_HEALTH.value
        
        case TransactionName.AH.value:
            name = TransactionName.ADVENT.value
        
        case TransactionName.INTEREST_EARNED.value:
            name = TransactionName.INTEREST.value
        
        case TransactionName.HEALTH_ONE.value:
            name = TransactionName.SWEDISH.value
        
        case _:
            name = result[0]
    
    return transaction, name, amount
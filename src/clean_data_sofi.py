import pandas as pd
import re

from project_enums import TransactionName, TransactionType

def clean_data_sofi(csv_path: str) -> pd.DataFrame:
    df = clean_csv(csv_path)
    df[['Transaction', 'Name', 'Amount']] = df.apply(clean_name, axis=1).apply(pd.Series)
    return df

def clean_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.drop(['Current balance', 'Status'], axis=1, inplace=True)
    df = df[
        (df['Description'] != 'CARDMEMBER SERV') & 
        (df['Description'] != 'FID BKG SVC LLC') & 
        (df['Description'] != 'CITI CARD ONLINE') &
        (df['Type'] != 'Deposit') & 
        (df['Type'] != 'Withdrawal')
        ]
    df.rename(columns={'Description' : 'Name'}, inplace=True)
    df.insert(1, 'Transaction', df.pop('Type'))
    df['Amount'] = df['Amount'].mask(df['Amount'] < 0, df['Amount'] * -1, axis=0)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    return df

def clean_name(row: pd.DataFrame) -> tuple[str, float]:
    name = row['Name']
    amount = row['Amount']
    name = name.upper()
    transaction = row['Transaction']
    if transaction == TransactionName.DIRECT_DEPOSIT.value or transaction.upper() == TransactionName.INTEREST_EARNED.value:
        transaction = TransactionType.CREDIT.value
    else:
        transaction = TransactionType.DEBIT.value
        
    result = re.split(r'[*#\d\.-]', name)

    match result[0]:
        case TransactionName.LIBERTY_MUTUAL.value:
            if amount < 75.00:
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
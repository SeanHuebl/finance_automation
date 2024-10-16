import pandas as pd
import re

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
    df['Amount'].mask(df['Amount'] < 0, df['Amount'] * -1, inplace=True, axis=0)
    return df
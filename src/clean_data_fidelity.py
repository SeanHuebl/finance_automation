import pandas as pd
import re

from project_enums import PaidOff, TransactionName, TransactionType

def clean_data_fidelity(csv_path: str) -> pd.DataFrame:
    df = clean_csv(csv_path)
    # Otherwise dropping mid loop changes the index size resulting in error at the end
    rows_to_drop = []
    for i in range(df.shape[0]):
        if df.iloc[i, 2][:22] == PaidOff.PAYMENT.value:
            rows_to_drop.append(i)
        df = split_transaction_name(fix_amount(fix_date(df, i), i), i)
        clean_transaction_name(df, i)
    df.drop(rows_to_drop, inplace=True)
    return df


def clean_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.drop('Memo', axis=1)
    return df

def fix_date(df: pd.DataFrame, i: int) -> pd.DataFrame:
    date = df.iloc[i, 0].split('-')
    date.append(date.pop(0))
    date = '-'.join(date)
    df.iloc[i, 0] = date
    return df
    
def fix_amount(df: pd.DataFrame, i: int) -> pd.DataFrame:
    if df.iloc[i, 1] == TransactionType.DEBIT.value:
        df.iloc[i, 3] = df.iloc[i, 3] * -1
    return df

def split_transaction_name(df: pd.DataFrame, i: int) -> pd.DataFrame:
    df.iloc[i, 2] = df.iloc[i, 2][:22]
    return df

def clean_transaction_name(df: pd.DataFrame, i: int) -> pd.DataFrame:
    name = df.iloc[i, 2]
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
            
    print(name)
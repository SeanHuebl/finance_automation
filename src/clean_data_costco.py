import pandas as pd
import re

from project_enums import PaidOff, TransactionName

def clean_data_costco(csv_path: str) -> pd.DataFrame:
    df = clean_csv(csv_path)
    df = df[df['Name'] != PaidOff.COSTCO_PAYMENT.value]
    df['Name'] = df.apply(clean_transaction_name, axis=1)
    return df

def clean_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.drop(['Status', 'Member Name'], axis=1)
    df['Transaction'] = ['DEBIT' if not pd.isna(a) else 'CREDIT' for a in df['Debit']]
    col = df.pop('Transaction')
    df.insert(1, 'Transaction', col)
    df = df.rename(columns={'Description': 'Name'})
    df['Amount'] = [a if not pd.isna(a) else b * -1 for a, b in zip(df['Debit'], df['Credit'])]
    df = df.drop(['Debit', 'Credit'], axis=1)
    return df

def clean_transaction_name(row: pd.DataFrame) -> str:
    name = row['Name']
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
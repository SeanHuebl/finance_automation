import pandas as pd

from project_enums import Category, TransactionType

# Categorizes all transactions unless transaciton would fall into OTHER category
transaction_dict = {
    'Rover' : Category.PET,
    'RX PLUS PHARMACY' : Category.MEDICAL,
    'GROOMER' : Category.PET,
    'WAGTOPIA' : Category.PET,
    'COSTCO' : Category.FOOD,
    'KING SOOPERS' : Category.FOOD,
    'RENTERS INSURANCE' : Category.HOUSING,
    'RENT' : Category.HOUSING,
    'CAR INSURANCE' : Category.HOUSING,
    'VET' : Category.PET,
    'COSTCO GAS': Category.CAR,
    'SAFEWAY' : Category.FOOD,
    'CRUNCHYROLL' : Category.SUBSCRIPTIONS,
    'CAR PAYMENT' : Category.CAR,
    'AMAZON PRIME' : Category.SUBSCRIPTIONS,
    'SHELL OIL' : Category.CAR,
    'SPOTIFY' : Category.SUBSCRIPTIONS,
    'XFINITY MOBILE' : Category.UTILITIES,
    'HEADWAY' : Category.MEDICAL,
    'XCEL ENERGY' : Category.UTILITIES,
    'HULU' : Category.SUBSCRIPTIONS,
    'SPOT PET INSURANCE' : Category.PET
}

def categorize_data_income(combined_df: pd.DataFrame) -> pd.DataFrame:
    income_df = combined_df[combined_df['Transaction'] == TransactionType.CREDIT.value].copy()
    income_df.loc[:, 'Category'] = Category.INCOME.value
    return income_df

def categorize_data_expenses(combined_df: pd.DataFrame) -> pd.DataFrame:
    expenses_df = combined_df[combined_df['Transaction'] == TransactionType.DEBIT.value].copy()
    expenses_df.loc[:, 'Category'] = expenses_df.apply(category_lookup, axis=1)
    return expenses_df

def category_lookup(row: pd.DataFrame) -> str:
    if row['Name'] in transaction_dict:
        return transaction_dict[row['Name']].value
    else:
        return Category.OTHER.value
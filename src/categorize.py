import pandas as pd

from project_enums import Category, TransactionType

# Categorizes all transactions unless transaciton would fall into OTHER category
transaction_dict: dict = {
    'ROVER' : Category.PET,
    'RX PLUS PHARMACY' : Category.MEDICAL,
    'GROOMER' : Category.PET,
    'WAGTOPIA' : Category.PET,
    'COSTCO' : Category.FOOD,
    'KING SOOPERS' : Category.FOOD,
    'RENTERS INSURANCE' : Category.HOUSING,
    'RENT' : Category.HOUSING,
    'CAR INSURANCE' : Category.CAR,
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
    'SPOT PET INSURANCE' : Category.PET,
    'INTERNET' : Category.UTILITIES
}

def _categorize_data_income(combined_df: pd.DataFrame) -> pd.DataFrame:
    if combined_df.empty or not isinstance(combined_df, pd.DataFrame):
        raise ValueError('Arg: combined_df must not be empty and must be of class pd.DataFrame')
    income_df: pd.DataFrame = combined_df[combined_df['Transaction'] == TransactionType.CREDIT.value].copy()
    income_df.loc[:, 'Category'] = Category.INCOME.value
    return income_df

def _categorize_data_expenses(combined_df: pd.DataFrame) -> pd.DataFrame:
    if combined_df.empty or not isinstance(combined_df, pd.DataFrame):
        raise ValueError('Arg: combined_df must not be empty and must be of class pd.DataFrame')
    expenses_df: pd.DataFrame = combined_df[combined_df['Transaction'] == TransactionType.DEBIT.value].copy()
    expenses_df.loc[:, 'Category'] = expenses_df.apply(_category_lookup, axis=1)
    return expenses_df

def _category_lookup(row: pd.DataFrame) -> str:
    if row.empty or not isinstance(row, pd.DataFrame):
        raise ValueError('Arg: row must not be empty and must be of class pd.DataFrame')
    if row['Name'] in transaction_dict:
        return transaction_dict[row['Name']].value
    else:
        return Category.OTHER.value
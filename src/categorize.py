import pandas as pd

from project_enums import Category, TransactionType

# Mapping of transaction names to their respective categories
transaction_dict: dict = {
    'ROVER': Category.PET,
    'RX PLUS PHARMACY': Category.MEDICAL,
    'GROOMER': Category.PET,
    'WAGTOPIA': Category.PET,
    'COSTCO': Category.FOOD,
    'KING SOOPERS': Category.FOOD,
    'RENTERS INSURANCE': Category.HOUSING,
    'RENT': Category.HOUSING,
    'CAR INSURANCE': Category.CAR,
    'VET': Category.PET,
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
    """
    Categorizes income transactions in the given DataFrame.

    This function filters transactions classified as 'CREDIT' and assigns them to 
    the 'INCOME' category.

    Args:
        combined_df (pd.DataFrame): A DataFrame containing transaction data.

    Returns:
        pd.DataFrame: A DataFrame containing only income transactions with a 'Category' column set to 'INCOME'.

    Raises:
        ValueError: If the `combined_df` is empty or not of type `pd.DataFrame`.
    """
    if combined_df.empty or not isinstance(combined_df, pd.DataFrame):
        raise ValueError('Arg: combined_df must not be empty and must be of class pd.DataFrame')

    # Filter transactions classified as 'CREDIT' and set their category to 'INCOME'
    income_df: pd.DataFrame = combined_df[combined_df['Transaction'] == TransactionType.CREDIT.value].copy()
    income_df.loc[:, 'Category'] = Category.INCOME.value

    return income_df

def _categorize_data_expenses(combined_df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorizes expense transactions in the given DataFrame.

    This function filters transactions classified as 'DEBIT' and categorizes them 
    based on predefined mappings in `transaction_dict`. Transactions not found 
    in the dictionary are categorized as 'OTHER'.

    Args:
        combined_df (pd.DataFrame): A DataFrame containing transaction data.

    Returns:
        pd.DataFrame: A DataFrame containing only expense transactions with a 'Category' column assigned.

    Raises:
        ValueError: If the `combined_df` is empty or not of type `pd.DataFrame`.
    """
    if combined_df.empty or not isinstance(combined_df, pd.DataFrame):
        raise ValueError('Arg: combined_df must not be empty and must be of class pd.DataFrame')

    # Filter transactions classified as 'DEBIT' and categorize them based on `transaction_dict`
    expenses_df: pd.DataFrame = combined_df[combined_df['Transaction'] == TransactionType.DEBIT.value].copy()
    expenses_df.loc[:, 'Category'] = expenses_df.apply(_category_lookup, axis=1)

    return expenses_df

def _category_lookup(row: pd.Series) -> str:
    """
    Looks up and assigns a category to a transaction based on its 'Name'.

    This function checks the transaction's 'Name' in `transaction_dict` and returns 
    the corresponding category. If not found, it assigns the category as 'OTHER'.

    Args:
        row (pd.DataFrame): A single row of the DataFrame containing transaction data.

    Returns:
        str: The category of the transaction.

    Raises:
        ValueError: If the `row` is empty or not of type `pd.DataFrame`.
    """
    if row.empty or not isinstance(row, pd.Series):
        raise ValueError('Arg: row must not be empty and must be of class pd.DataFrame')

    # Check if the transaction name exists in the dictionary and assign its category
    if row['Name'] in transaction_dict:
        return transaction_dict[row['Name']].value
    else:
        return Category.OTHER.value
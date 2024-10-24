import os
import pandas as pd
import re

from project_enums import TransactionName, TransactionType
from typing import List

def clean_data_sofi(csv_path: str) -> pd.DataFrame:
    """
    Cleans the SoFi CSV file and standardizes the data for further processing.

    This function reads a SoFi CSV file, processes the data to clean and standardize 
    the names and transactions, and returns a cleaned DataFrame.

    Args:
        csv_path (str): The file path to the SoFi CSV file.

    Returns:
        pd.DataFrame: A cleaned DataFrame with standardized columns and values.

    Raises:
        ValueError: If the `csv_path` is not a valid string or file path, or if it is not a CSV file.
    """
    if not csv_path or not isinstance(csv_path, str):
        raise ValueError('Arg: csv_path must exist and be of type str')
    if not os.path.exists(csv_path):
        raise ValueError('Arg: csv_path must be a valid file path')
    if not csv_path.endswith('.csv'):
        raise ValueError('Arg: csv_path must be of file type .csv')

    # Read and clean the raw CSV data
    df: pd.DataFrame = _clean_csv(csv_path)

    # Apply `_clean_name` to each row to standardize 'Transaction', 'Name', and 'Amount' columns
    df[['Transaction', 'Name', 'Amount']] = df.apply(_clean_name, axis=1).apply(pd.Series)
    
    return df

def _clean_csv(csv_path: str) -> pd.DataFrame:
    """
    Reads and cleans the raw CSV file, removing unnecessary data and standardizing columns.

    Args:
        csv_path (str): The file path to the CSV file.

    Returns:
        pd.DataFrame: A cleaned DataFrame with updated column names and standardized values.

    Raises:
        ValueError: If the `csv_path` is not a valid string or file path, or if it is not a CSV file.
    """
    if not csv_path or not isinstance(csv_path, str):
        raise ValueError('Arg: csv_path must exist and be of type str')
    if not os.path.exists(csv_path):
        raise ValueError('Arg: csv_path must be a valid file path')
    if not csv_path.endswith('.csv'):
        raise ValueError('Arg: csv_path must be of file type .csv')

    df: pd.DataFrame = pd.read_csv(csv_path)
    
    # Drop columns that are not needed for analysis
    df.drop(['Current balance', 'Status'], axis=1, inplace=True)
    
    # Filter out unwanted rows based on specific descriptions and transaction types
    df = df[
        (df['Description'] != 'CARDMEMBER SERV') & 
        (df['Description'] != 'FID BKG SVC LLC') & 
        (df['Description'] != 'CITI CARD ONLINE') &
        (df['Type'] != 'Deposit') & 
        (df['Type'] != 'Withdrawal')
    ].copy()
    
    # Rename 'Description' to 'Name' for consistency
    df.rename(columns={'Description': 'Name'}, inplace=True)

    # Move 'Type' to 'Transaction' column for clarity and reorganization
    df.insert(1, 'Transaction', df.pop('Type'))

    # Standardize the 'Amount' column by converting negative amounts to positive for easier analysis
    df['Amount'] = df['Amount'].mask(df['Amount'] < 0, df['Amount'] * -1, axis=0)

    # Convert date format to MM/DD/YYYY for consistency
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    
    return df

def _clean_name(row: pd.DataFrame) -> tuple[str, str, float]:
    """
    Cleans and standardizes transaction names based on predefined patterns.

    Args:
        row (pd.DataFrame): A single row of the DataFrame containing transaction data.

    Returns:
        tuple[str, str, float]: A tuple containing the cleaned transaction type, standardized name, and amount.

    Raises:
        ValueError: If the `row` is empty or not of type `pd.DataFrame`.
    """
    if row.empty or not isinstance(row, pd.DataFrame):
        raise ValueError('Arg: row must not be empty and must be of class pd.DataFrame')

    transaction: str = row['Transaction']
    name: str = row['Name']
    amount: float = row['Amount']

    # Convert the name to uppercase for consistency
    name = name.upper()

    # Standardize the transaction type based on predefined conditions
    if transaction == TransactionName.DIRECT_DEPOSIT.value or transaction.upper() == TransactionName.INTEREST_EARNED.value:
        transaction = TransactionType.CREDIT.value
    else:
        transaction = TransactionType.DEBIT.value

    # Remove unwanted characters and split name into meaningful parts
    result: List[str] = re.split(r'[*#\d\.-]', name)

    # Match against predefined patterns to standardize common transaction names
    match result[0]:
        case TransactionName.LIBERTY_MUTUAL.value:
            # Determine insurance type based on the transaction amount
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
            # Use the first part of the name by default if no specific pattern is matched
            name = result[0]
    
    return transaction, name, amount
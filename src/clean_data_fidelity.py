import os
import pandas as pd
import re

from project_enums import PaidOff, TransactionName, TransactionType

def clean_data_fidelity(csv_path: str) -> pd.DataFrame:
    """
    Cleans the Fidelity CSV file and standardizes the data for further processing.

    This function reads a Fidelity CSV file, processes the data to remove specific entries, 
    fix dates and amounts, and standardize transaction names. It returns a cleaned DataFrame.

    Args:
        csv_path (str): The file path to the Fidelity CSV file.

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

    # Truncate 'Name' column to a maximum of 22 characters for consistency
    df['Name'] = df['Name'].str[:22]

    # Remove specific entries marked as payments to Fidelity
    df = df[df['Name'] != PaidOff.FIDELITY_PAYMENT.value]

    # Apply `_fix_date` to each row to standardize the date format
    df['Date'] = df.apply(_fix_date, axis=1)

    # Apply `_fix_amount` to each row to correct negative amounts for debits
    df['Amount'] = df.apply(_fix_amount, axis=1)

    # Apply `_clean_transaction_name` to each row to standardize the 'Name' column
    df['Name'] = df.apply(_clean_transaction_name, axis=1)

    return df


def _clean_csv(csv_path: str) -> pd.DataFrame:
    """
    Reads and cleans the raw CSV file, removing unnecessary columns.

    Args:
        csv_path (str): The file path to the CSV file.

    Returns:
        pd.DataFrame: A cleaned DataFrame with unnecessary columns removed.

    Raises:
        ValueError: If the `csv_path` is not a valid string or file path, or if it is not a CSV file.
    """
    if not csv_path or not isinstance(csv_path, str):
        raise ValueError('Arg: csv_path must exist and be of type str')
    if not os.path.exists(csv_path):
        raise ValueError('Arg: csv_path must be a valid file path')
    if not csv_path.endswith('.csv'):
        raise ValueError('Arg: csv_path must be of file type .csv')

    df = pd.read_csv(csv_path)

    # Drop the 'Memo' column as it does not contribute to financial analysis
    return df.drop('Memo', axis=1)

def _fix_date(row: pd.DataFrame) -> str:
    """
    Fixes the date format to MM/DD/YYYY for consistency.

    Args:
        row (pd.DataFrame): A single row of the DataFrame containing transaction data.

    Returns:
        str: The formatted date as a string in MM/DD/YYYY format.

    Raises:
        ValueError: If the `row` is empty or not of type `pd.DataFrame`.
    """
    if row.empty or not isinstance(row, pd.DataFrame):
        raise ValueError('Arg: row must not be empty and must be of class pd.DataFrame')

    date: pd.Timestamp = pd.to_datetime(row['Date'], format='%Y-%m-%d')
    return date.strftime('%m/%d/%Y')
    
def _fix_amount(row: pd.DataFrame) -> float:
    """
    Adjusts the 'Amount' value based on the transaction type.

    If the transaction is of type 'DEBIT', the amount is made negative. Otherwise, it remains unchanged.

    Args:
        row (pd.DataFrame): A single row of the DataFrame containing transaction data.

    Returns:
        float: The corrected amount.

    Raises:
        ValueError: If the `row` is empty or not of type `pd.DataFrame`.
    """
    if row.empty or not isinstance(row, pd.DataFrame):
        raise ValueError('Arg: row must not be empty and must be of class pd.DataFrame')

    if row['Transaction'] == TransactionType.DEBIT.value:
        return row['Amount'] * -1
    return row['Amount']
    
def _clean_transaction_name(row: pd.DataFrame) -> str:
    """
    Cleans and standardizes transaction names based on predefined patterns.

    Args:
        row (pd.DataFrame): A single row of the DataFrame containing transaction data.

    Returns:
        str: A standardized transaction name.

    Raises:
        ValueError: If the `row` is empty or not of type `pd.DataFrame`.
    """
    if row.empty or not isinstance(row, pd.DataFrame):
        raise ValueError('Arg: row must not be empty and must be of class pd.DataFrame')

    name: str = row['Name']

    # Remove unwanted characters and extract the meaningful portion of the name
    result = re.split(r'[*#\d\.-]', name)

    # Match transaction names with predefined patterns for standardization
    match result[0]:
        case TransactionName.PAYPAL.value:
            # Strip trailing whitespace for consistency
            name = result[1].rstrip()
            # Rename Starbucks shorthand to standard format
            if name == TransactionName.STARBUCKSSE.value:
                name = TransactionName.STARBUCKS.value

        case TransactionName.CPI.value:
            name = TransactionName.VENDING_MACHINE.value

        case TransactionName.VC.value:
            name = TransactionName.VET.value

        case TransactionName.SQ.value:
            # Strip trailing whitespace and standardize the groomer's name
            name = result[1].rstrip()
            if name == TransactionName.A_CLIP_ABOVE.value:
                name = TransactionName.GROOMER.value

        case TransactionName.AMAZON_PRIME.value:
            # Ensure Amazon Prime is consistently capitalized
            name = TransactionName.AMAZON_PRIME.value.upper()

        case _:
            # Use the first extracted portion, stripping trailing whitespace and converting to uppercase
            name = result[0].rstrip().upper()

            # Check if the name contains any substring related to 'Amazon' and standardize it
            for substring in TransactionName.AMAZON.value:
                if substring in name:
                    name = TransactionName.AMAZON.value[0]

            # Standardize Costco-related transactions
            if TransactionName.COSTCO.value in name:
                name = TransactionName.COSTCO.value
            
    return name
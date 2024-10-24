import os
import pandas as pd
import re

from project_enums import PaidOff, TransactionName

def clean_data_costco(csv_path: str) -> pd.DataFrame:
    """
    Cleans the Costco CSV file and standardizes the data for further processing.

    This function reads a Costco CSV file, processes the data to remove specific entries 
    and standardize transaction names, and returns a cleaned DataFrame.

    Args:
        csv_path (str): The file path to the Costco CSV file.

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

    # Clean the CSV data
    df: pd.DataFrame = _clean_csv(csv_path)

    # Remove entries associated with Costco payments, as these are not considered transactions
    df = df[df['Name'] != PaidOff.COSTCO_PAYMENT.value]

    # Apply `_clean_transaction_name` to each row to standardize the 'Name' column
    df['Name'] = df.apply(_clean_transaction_name, axis=1)

    return df

def _clean_csv(csv_path: str) -> pd.DataFrame:
    """
    Reads and cleans the raw CSV file, removing unnecessary columns and standardizing values.

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

    # Drop unnecessary columns that do not contribute to financial analysis
    df = df.drop(['Status', 'Member Name'], axis=1)

    # Determine transaction type ('DEBIT' or 'CREDIT') based on values in 'Debit' column
    df['Transaction'] = ['DEBIT' if not pd.isna(a) else 'CREDIT' for a in df['Debit']]

    # Move 'Transaction' to the second column for better organization
    col = df.pop('Transaction')
    df.insert(1, 'Transaction', col)

    # Rename 'Description' to 'Name' for consistency in naming conventions
    df = df.rename(columns={'Description': 'Name'})

    # Calculate 'Amount' based on 'Debit' or the negative of the value in 'Credit' for consistency
    df['Amount'] = [a if not pd.isna(a) else b * -1 for a, b in zip(df['Debit'], df['Credit'])]

    # Drop the 'Debit' and 'Credit' columns, as their information has been consolidated into 'Amount'
    df = df.drop(['Debit', 'Credit'], axis=1)

    return df

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

            # Standardize wax-related transactions
            if TransactionName.WAX.value in name:
                name = TransactionName.WAX.value

    return name
import pandas as pd

from clean_data_fidelity import clean_data_fidelity
from clean_data_costco import clean_data_costco
from clean_data_sofi import clean_data_sofi
from categorize import _categorize_data_expenses, _categorize_data_income

def wrangle_data() -> pd.DataFrame:
    """
    Cleans, combines, categorizes, and sorts transaction data from multiple sources.

    This function orchestrates the entire data processing workflow by combining cleaned data 
    from multiple sources, categorizing transactions as either income or expenses, and sorting 
    the final data by date.

    Returns:
        pd.DataFrame: A fully cleaned, categorized, and sorted DataFrame.
    """
    return _fix_time_and_sort(_categorize_data(_combine_data()))


def _combine_data() -> pd.DataFrame:
    """
    Combines cleaned data from multiple CSV files into a single DataFrame.

    This function reads, cleans, and concatenates data from Fidelity, Costco, and SoFi CSV files.

    Returns:
        pd.DataFrame: A combined DataFrame containing cleaned data from all sources.
    """
    df_fidelity: pd.DataFrame = clean_data_fidelity('./test_csv/fidelity.csv')
    df_costco: pd.DataFrame = clean_data_costco('./test_csv/costco.csv')
    df_sofi: pd.DataFrame = clean_data_sofi('./test_csv/sofi.csv')

    # Concatenate all cleaned data into a single DataFrame
    combined_df: pd.DataFrame = pd.concat([df_fidelity, df_costco, df_sofi])

    return combined_df
    
def _categorize_data(combined_df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorizes the combined transaction data into income and expenses.

    This function splits the combined DataFrame into income and expense transactions,
    applies category labels to each transaction, and then merges the results.

    Args:
        combined_df (pd.DataFrame): A combined DataFrame containing all transaction data.

    Returns:
        pd.DataFrame: A DataFrame with categorized income and expenses.

    Raises:
        ValueError: If the `combined_df` is empty or not of type `pd.DataFrame`.
    """
    if combined_df.empty or not isinstance(combined_df, pd.DataFrame):
        raise ValueError('Arg: combined_df must not be empty and must be of class pd.DataFrame')

    # Categorize income and expenses separately
    df_income: pd.DataFrame = _categorize_data_income(combined_df)
    df_expenses: pd.DataFrame = _categorize_data_expenses(combined_df)

    # Combine the categorized income and expenses into a single DataFrame
    combined_df: pd.DataFrame = pd.concat([df_income, df_expenses])

    return combined_df

def _fix_time_and_sort(combined_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fixes date formatting and sorts the combined DataFrame by date.

    This function converts the date column to a standard format, sorts transactions 
    by date, and resets the index.

    Args:
        combined_df (pd.DataFrame): A combined DataFrame containing categorized transaction data.

    Returns:
        pd.DataFrame: A sorted DataFrame with date formatting fixed.

    Raises:
        ValueError: If the `combined_df` is empty or not of type `pd.DataFrame`.
    """
    if combined_df.empty or not isinstance(combined_df, pd.DataFrame):
        raise ValueError('Arg: combined_df must not be empty and must be of class pd.DataFrame')

    # Convert 'Date' column to datetime objects and sort the DataFrame by date
    combined_df['Date'] = pd.to_datetime(combined_df['Date'], format='%m/%d/%Y')
    df_transactions: pd.DataFrame = combined_df.sort_values(by='Date').reset_index(drop=True)

    # Reformat the 'Date' column to the standard MM/DD/YYYY format
    df_transactions['Date'] = df_transactions['Date'].dt.strftime('%m/%d/%Y')

    return df_transactions
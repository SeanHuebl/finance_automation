import pandas as pd

from clean_data_fidelity import clean_data_fidelity
from clean_data_costco import clean_data_costco
from clean_data_sofi import clean_data_sofi
from categorize import _categorize_data_expenses, _categorize_data_income

def wrangle_data() -> pd.DataFrame:
    return _fix_time_and_sort(_categorize_data(_combine_data()))


def _combine_data() -> pd.DataFrame:
    df_fidelity: pd.DataFrame = clean_data_fidelity('./test_csv/fidelity.csv')
    df_costco: pd.DataFrame = clean_data_costco('./test_csv/costco.csv')
    df_sofi: pd.DataFrame = clean_data_sofi('./test_csv/sofi.csv')
    combined_df: pd.DataFrame = pd.concat([df_fidelity, df_costco, df_sofi])
    return combined_df
    
def _categorize_data(combined_df: pd.DataFrame) -> pd.DataFrame:
    if combined_df.empty or not isinstance(combined_df, pd.DataFrame):
        raise ValueError('Arg: combined_df must not be empty and must be of class pd.DataFrame')
    df_income: pd.DataFrame = _categorize_data_income(combined_df)
    df_expenses: pd.DataFrame = _categorize_data_expenses(combined_df)
    combined_df: pd.DataFrame = pd.concat([df_income, df_expenses])
    return combined_df

def _fix_time_and_sort(combined_df: pd.DataFrame) -> pd.DataFrame:
    if combined_df.empty or not isinstance(combined_df, pd.DataFrame):
        raise ValueError('Arg: combined_df must not be empty and must be of class pd.DataFrame')
    combined_df['Date'] = pd.to_datetime(combined_df['Date'], format='%m/%d/%Y')
    df_transactions: pd.DataFrame = combined_df.sort_values(by='Date')
    df_transactions = df_transactions.reset_index(drop=True)
    df_transactions['Date'] = df_transactions['Date'].dt.strftime('%m/%d/%Y')
    return df_transactions
import pandas as pd

from project_enums import Category, TransactionType

def categorize_data(combined_df: pd.DataFrame) -> pd.DataFrame:
    income_df = combined_df[combined_df['Transaction'] == TransactionType.CREDIT.value]
    income_df['Category'] = Category.INCOME.value
    return income_df
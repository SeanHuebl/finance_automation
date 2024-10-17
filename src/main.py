import pandas as pd
from clean_data_fidelity import clean_data_fidelity
from clean_data_costco import clean_data_costco
from clean_data_sofi import clean_data_sofi
from categorize import categorize_data

def combine_data() -> pd.DataFrame:
    df_fidelity = clean_data_fidelity('./test_csv/fidelity.csv')
    df_costco = clean_data_costco('./test_csv/costco.csv')
    df_sofi = clean_data_sofi('./test_csv/sofi.csv')
    df_combined = pd.concat([df_fidelity, df_costco, df_sofi])
    df_combined['Date'] = pd.to_datetime(df_combined['Date'], format='%m/%d/%Y')
    df_transactions = df_combined.sort_values(by='Date')
    df_transactions = df_transactions.reset_index(drop=True)
    df_transactions['Date'] = df_transactions['Date'].dt.strftime('%m/%d/%Y')
    return df_transactions

def main():
    pd.set_option('display.max_rows', None)
    df = combine_data()
    df = categorize_data(df)
    print(df)
    pd.reset_option('display.max_rows')
if __name__ == '__main__':
    main()
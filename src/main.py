import pandas as pd
from clean_data_fidelity import clean_data_fidelity

def main():
    pd.set_option('display.max_rows', None)
    df = clean_data_fidelity('./test_csv/large.csv')
    print(df)
    pd.reset_option('display.max_rows')
if __name__ == '__main__':
    main()
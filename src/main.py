import pandas as pd

from wrangle_data import wrangle_data

def main():
    
    pd.set_option('display.max_rows', None)
    df = wrangle_data()
    print(df)
    pd.reset_option('display.max_rows')

if __name__ == '__main__':
    main()
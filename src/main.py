import pandas as pd

from googleapiclient.discovery import build
from google_cloud import get_credentials, write_data
from wrangle_data import wrangle_data

def main():
    
    pd.set_option('display.max_rows', None)
    df = wrangle_data()
    
    credentials = get_credentials()
    service = build('sheets', 'v4', credentials=credentials)
    spreadsheet_id = '1T_-oDRsrrKe0pmfGlSkh59K80fc3AmMVJphW7OEh09A'
    result = write_data(service, 'Food', spreadsheet_id, df)
    print(result)
    pd.reset_option('display.max_rows')

if __name__ == '__main__':
    main()
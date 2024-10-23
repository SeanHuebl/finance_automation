import pandas as pd

from googleapiclient.discovery import build, Resource
from google.oauth2.credentials import Credentials

from google_cloud import get_credentials, write_data
from project_enums import Category
from wrangle_data import wrangle_data

def main():

    df: pd.DataFrame = wrangle_data()
    credentials: Credentials = get_credentials()
    service: Resource = build('sheets', 'v4', credentials=credentials)
    spreadsheet_id: str = '1T_-oDRsrrKe0pmfGlSkh59K80fc3AmMVJphW7OEh09A'
    
    for _ in Category:
        write_data(service, _.value.capitalize(), spreadsheet_id, df)

if __name__ == '__main__':
    main()
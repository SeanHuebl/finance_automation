import pandas as pd

from googleapiclient.discovery import build, Resource
from google.oauth2.credentials import Credentials

from google_cloud import get_credentials, write_data
from project_enums import Category
from wrangle_data import wrangle_data

def main() -> None:
    """
    Main function to clean, categorize, and upload transaction data to a Google Spreadsheet.

    This function performs the following tasks:
    1. Wrangles the transaction data by cleaning and categorizing it.
    2. Obtains Google Sheets API credentials via OAuth 2.0.
    3. Creates a Google Sheets API service resource.
    4. Iterates through all defined categories and uploads the filtered data to the Google Sheet.

    Raises:
        Exception: If any errors occur during the API call or data processing.
    """
    # Wrangle and clean the transaction data
    df: pd.DataFrame = wrangle_data()

    # Obtain OAuth 2.0 credentials for Google Sheets API
    credentials: Credentials = get_credentials()

    # Build the Google Sheets API service resource
    service: Resource = build('sheets', 'v4', credentials=credentials)

    # Specify the Google Spreadsheet ID to write data to
    spreadsheet_id: str = '1T_-oDRsrrKe0pmfGlSkh59K80fc3AmMVJphW7OEh09A'

    # Iterate through each category and upload the corresponding data to the Google Sheet
    for category in Category:
        # Capitalize the category name to match the Google Sheet tab name
        write_data(service, category.value.capitalize(), spreadsheet_id, df)

if __name__ == '__main__':
    main()
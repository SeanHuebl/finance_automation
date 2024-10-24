import pandas as pd

from googleapiclient.discovery import Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from typing import List

# Project and secret identifiers
PROJECT_ID: str = '438040797905'
SECRET_ID: str = 'sheets_access'
SCOPES: List[str] = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials() -> Credentials:
    """
    Obtains OAuth 2.0 credentials for accessing the Google Sheets API.

    This function uses OAuth 2.0 installed app flow to obtain credentials for accessing
    the Google Sheets API, allowing the user to authorize access through their Google account.

    Returns:
        Credentials: An authorized credentials object for accessing the Google Sheets API.
    """
    # Initialize the OAuth flow with client secrets and the required scopes
    flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
        './sensitive/client_secret_desktop.json', SCOPES
    )
    # Run the local server to obtain user authorization and get the credentials
    creds = flow.run_local_server(port=0)
    return creds


def write_data(service: Resource, sheet_name: str, spreadsheet_id: str, df: pd.DataFrame) -> None:
    """
    Writes data from a DataFrame to a specific Google Sheet.

    This function filters the provided DataFrame by a specific category, removes unnecessary columns,
    and writes the resulting data to a specific Google Sheet. The sheet range is determined based on 
    the provided sheet name.

    Args:
        service (Resource): An authorized Google Sheets API service resource.
        sheet_name (str): The name of the Google Sheet tab where the data should be written.
        spreadsheet_id (str): The ID of the Google Spreadsheet.
        df (pd.DataFrame): A DataFrame containing the data to be written to the sheet.

    Raises:
        ValueError: If any of the provided arguments are invalid or if the DataFrame is empty.

    Prints:
        The number of cells updated in the specified sheet.
    """
    # Validate the service object and other input arguments
    if not service or not isinstance(service, Resource):
        raise ValueError('Arg: service must exist and be of class Resource')
    if not sheet_name or not isinstance(sheet_name, str):
        raise ValueError('Arg: sheet_name must exist and be of type str')
    if not spreadsheet_id or not isinstance(spreadsheet_id, str):
        raise ValueError('Arg: spreadsheet_id must exist and be of type str')
    if df.empty or not isinstance(df, pd.DataFrame):
        raise ValueError('Arg: df must not be empty and must be of class pd.DataFrame')

    # Convert the sheet name to uppercase to match the 'Category' column in the DataFrame
    category: str = sheet_name.upper()

    # Filter the DataFrame by the specified category and drop unnecessary columns
    df: pd.DataFrame = df[df['Category'] == category].copy().drop(['Transaction', 'Category'], axis=1)

    # Convert the filtered DataFrame to a list of lists for Google Sheets API
    values: List[List] = df.apply(lambda row: row.tolist(), axis=1).tolist()

    # Define the range in the sheet to write the values
    range_name: str = f'{sheet_name}!A2:C'
    body: dict = {'values': values}

    # Update the specified range in the sheet using the Google Sheets API
    results: dict = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    # Print the number of cells updated
    print(f"{results.get('updatedCells')} cells updated in {sheet_name}")
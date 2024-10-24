import pandas as pd

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource
from typing import List

PROJECT_ID: str = '438040797905'
SECRET_ID: str = 'sheets_access'
SCOPES: List[str] = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials() -> Credentials:

    flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file('./sensitive/client_secret_desktop.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds


def write_data(service: Resource, sheet_name: str, spreadsheet_id: str, df: pd.DataFrame) -> None:

    if not service or not isinstance(service, Resource):
        raise ValueError('Arg: service must exist and be of class Resource')
    if not sheet_name or not isinstance(sheet_name, str):
        raise ValueError('Arg: sheet_name must exist and be of type str')
    if not spreadsheet_id or not isinstance(spreadsheet_id, str):
        raise ValueError('Arg: spreadsheet_id must exist and be of type str')
    if df.empty or not isinstance(df, pd.DataFrame):
        raise ValueError('Arg: df must not be empty and must be of class pd.DataFrame')

    category: str = sheet_name.upper()    
    df: pd.DataFrame = df[df['Category'] == category].copy().drop(['Transaction', 'Category'], axis=1)

    values: List[List[str, str, float]] = df.apply(lambda row: row.tolist(), axis=1).tolist()
    range_name: str = f'{sheet_name}!A2:C'
    body: dict = {'values' : values}

    results: dict = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, 
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
        ).execute()
    
    print(f"{results.get('updatedCells')} cells updated in {sheet_name}")
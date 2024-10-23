import pandas as pd

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource
from typing import List
PROJECT_ID: str = '438040797905'
SECRET_ID: str = 'sheets_access'
SCOPES: List[str] = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials() -> Credentials:

    flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file('./sensitive/client_secret.json', SCOPES, redirect_uri='https://urban-space-parakeet-jw5w77vvprw2p4q5-8080.app.github.dev/')
    auth_url, _= flow.authorization_url(prompt='consent')
    
    print(f"Please go to this URL to authorize the app: {auth_url}")

    code: str = input("Enter the authorization code: ")

    flow.fetch_token(code=code)

    return flow.credentials


def write_data(service: Resource, sheet_name: str, spreadsheet_id: str, df: pd.DataFrame) -> None:

    if not service or not isinstance(service, Resource):
        raise ValueError('Arg: service must exist and be of class Resource')
    if not sheet_name or not isinstance(sheet_name, str):
        raise ValueError('Arg: sheet_name must exist and be of type str')
    if not spreadsheet_id or not isinstance(spreadsheet_id, str):
        raise ValueError('Arg: spreadsheet_id must exist and be of type str')
    if not df or not isinstance(df, pd.DataFrame):
        raise ValueError('Arg: df must exist and must be of class pd.Dataframe')

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
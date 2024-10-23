import pandas as pd

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource

PROJECT_ID = '438040797905'
SECRET_ID = 'sheets_access'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials() -> Credentials:

    flow = InstalledAppFlow.from_client_secrets_file('./sensitive/client_secret.json', SCOPES, redirect_uri='https://urban-space-parakeet-jw5w77vvprw2p4q5-8080.app.github.dev/')
    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f"Please go to this URL to authorize the app: {auth_url}")

    # After user authorizes, they will get an authorization code to paste here
    code = input("Enter the authorization code: ")

    # Manually fetch the token using the provided code
    flow.fetch_token(code=code)

    return flow.credentials


def write_data(service: Resource, sheet_name: str, spreadsheet_id: str, df: pd.DataFrame) -> None:
    category = sheet_name.upper()
    df = df[df['Category'] == category].copy().drop(['Transaction', 'Category'], axis=1)
    values = df.apply(lambda row: row.tolist(), axis=1).tolist()
    range_name = f'{sheet_name}!A2:C'
    body = {'values' : values}
    results = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, 
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
        ).execute()
    print(f"{results.get('updatedCells')} cells updated in {sheet_name}")
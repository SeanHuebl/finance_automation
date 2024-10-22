import os

from google.cloud import secretmanager
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource

PROJECT_ID = 'divine-fuze-439311-d6'
SECRET_ID = 'sheets_access'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def access_secret(version_id: str = 'latest') -> str:
    
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/{version_id}'

    response = client.access_secret_version(name=name)
    return response.payload.data.decode('utf-8')

def get_credentials() -> Credentials:
    client_secret = access_secret()

    with open('temp_client_secret.json', 'w') as secret_file:
        secret_file.write(client_secret)
    
    flow = InstalledAppFlow.from_client_secrets_file('temp_client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)

    os.remove('temp_client_secret.json')

    return creds

def write_data(service: Resource, sheet_name: str, spreadsheet_id: str) -> None:
    
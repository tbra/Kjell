from google.oauth2 import service_account
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service.json'

def calendar_credentials() -> service_account.Credentials:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return credentials

def calendar_service() -> Resource:
    try:
        service = build('calendar', 'v3', credentials=calendar_credentials())
        return service
    except HttpError as error:
        return error

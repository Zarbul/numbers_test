from __future__ import print_function

import os.path

from urllib.request import urlopen
from xml.etree import ElementTree as etree

from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from os import environ
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1x3q1Tkj4I_gViKM0SNQpMZwqN66QwoNDXDFuzU8oJR8'  # id google table
SAMPLE_RANGE_NAME = 'A2:D'  # table range

SECRET = environ.get("SECRET")  # client_secret.json
CLIENT_SECRET_FILE = settings.BASE_DIR / f'src/numbers/{SECRET}'
USER_TOKEN_FILE = settings.BASE_DIR / f'src/numbers/user_token.json'  # save token


def get_data_from_sheet():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(USER_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(USER_TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(USER_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        return values
    except HttpError as err:
        print(err)


def get_rate():
    with urlopen("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10) as r:
        rate = etree.parse(r).findtext('.//Valute[@ID="R01235"]/Value')
        return float(rate.replace(',', '.'))

import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# The permissions that this app will request
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_service(credentials_path="credentials.json", token_path="token.pickle"):
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service


def get_urls(service, spreadsheet_id):
    # Takes: a spreadsheet_id (the long string in the URL),
    # Returns: a list of strings for each non-empty cell in the row.
    # Largely copy-pasted from the quickstart.py example
    # TODO: Will need to be updated if the information moves to a different column
    SAMPLE_SPREADSHEET_ID = spreadsheet_id
    SAMPLE_RANGE_NAME = 'Livestream Info!D2:D300'

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()

    values = [url[0] for url in result.get('values', []) if url]

    if not values:
        raise Exception('No data found.')
    return values


def main():
    import sys
    if len(sys.argv) < 2:
        print("Required arguments: <GOOGLE_SHEET_ID>")
        sys.exit(1)
    service = get_service()
    print(get_urls(service, sys.argv[1]))


if __name__ == '__main__':
    main()

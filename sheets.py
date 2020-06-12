import json
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# The permissions that this app will request
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class Sheet():
    INFO_RANGE_NAME = 'Livestream Info!C1:D300'
    service = None
    sheet_id = None
    _cache = None

    def __init__(self, sheetid):
        self.service = get_service()
        self.sheet_id = sheetid

    def urls(self):
        return [r[1] for r in self._retrieve_sheet() if r and len(r) > 1]

    def update_status(self, url, status):
        new_status = "Live" if status else "Offline"
        # TODO: This is like the worst way to do this
        current_statuses = self._retrieve_sheet()
        for (row_id, row) in enumerate(current_statuses):
            if not row:
                continue
            sheet_status, sheet_url = row
            if url == sheet_url:
                if new_status != sheet_status:
                    self._set_cell_value(f"C{row_id+1}", new_status)
                return sheet_status == "Live"
        print("URL {} not found in sheet".format(url))
        raise Exception("URL {} not found in sheet".format(url))

    def _set_cell_value(self, cell, value):
        print(f"Setting {cell} to {value}")
        return self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range=f"Livestream Info!{cell}", body={"values": [[value]]}, valueInputOption="USER_ENTERED",
        ).execute()

    def _retrieve_sheet(self):
        if not self._cache:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheet_id,
                                        range=Sheet.INFO_RANGE_NAME).execute()
            self._cache = result['values']
        return self._cache


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


def main():
    import sys
    if len(sys.argv) < 2:
        print("Required arguments: <GOOGLE_SHEET_ID>")
        sys.exit(1)
    sheet = Sheet(sheetid=sys.argv[1])
    print(sheet.urls())


if __name__ == '__main__':
    main()

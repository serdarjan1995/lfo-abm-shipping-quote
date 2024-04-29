import gspread
from gspread import Client, Spreadsheet, Worksheet
from oauth2client.service_account import ServiceAccountCredentials


class GspreadClient:
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]

    def __init__(self, file_name='service-account.json'):
        self.file_name = file_name
        self.client = self._get_gspread_client()
        self.spreadsheet = None

    def _get_gspread_client(self) -> Client:
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.file_name, self.scope)
        client = gspread.authorize(creds)
        return client

    def open_spreadsheet(self, name: str) -> Spreadsheet:
        print(self.client.openall())
        self.spreadsheet = self.client.open(name)
        return self.spreadsheet

    def get_worksheet(self, sheet_name: str) -> Worksheet:
        if not self.spreadsheet:
            raise Exception("spreadsheet is not opened. call open_spreadsheet() first")
        return self.spreadsheet.worksheet(sheet_name)

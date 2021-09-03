import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

from data.config import CREDENTIALS_FILE

 
def connect(credentials_file):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    return service


def get_values(spreadsheet_id, range_):
    values = connect(CREDENTIALS_FILE).spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_,
        majorDimension='ROWS'
    ).execute()
    return values

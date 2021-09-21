import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from data.config import CREDENTIALS_FILE

 
async def connect(credentials_file):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http_auth)
    return service


async def get_values(spreadsheet_id, range_):
    service = await connect(CREDENTIALS_FILE)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_,
        majorDimension='ROWS'
    ).execute()
    return values

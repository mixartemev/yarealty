from __future__ import print_function
import pickle
import os.path
from pprint import pprint

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from db import session
from models.mcityOffer import McityOffer
from models.Offer import Offer

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1lPFc1p_5TNSxYOtJ4hSqcSMAiUig4slRQTdMmgJroic'


def to_sheet(offers: list):
    body = {'values': []}
    for o in offers:
        body['values'].append([
            o.id,
            o.cianUserId if o.cianUserId else '=HYPERLINK("https://www.mcity.ru/{}";"{}")'.format(o.idd, o.idd) if o.idd else None,
            o.bc.name if o.bc_id else None,
            o.house.name if o.house_id else None,
            o.newbuilding.name if o.newbuilding_id else None,
            o.description,
            str(o.creationDate),
            str(o.editDate),
            str(o.publishDate),
            o.category,
            o.dealType,
            o.status,
            o.bargainTerms_currency,
            o.price,
            o.pricePerUnitArea,
            o.floorNumber,
            str(o.totalArea),
            o.services,
            o.userTrust,
            o.isPro,
            o.stats_total,
            o.stats_daily,
            o.publishTerms_autoprolong,
        ])
    return body


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('sheet/token.pickle'):
        with open('sheet/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('sheet/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('sheet/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # # Create spreadsheet
    # spreadsheet = {'properties': {'title': 'MCity Cian Offers'}}
    # spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    # print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))

    mcityOffers = session.query(McityOffer).all()
    offers = session.query(Offer).all()

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range='mcity!A2', valueInputOption='USER_ENTERED', body=to_sheet(mcityOffers)
    ).execute()
    pprint(result)
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range='rival!A2', valueInputOption='USER_ENTERED', body=to_sheet(offers)
    ).execute()
    pprint(result)


if __name__ == '__main__':
    main()

import pickle
import os.path
from pprint import pprint
from typing import List
from datetime import date, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# If modifying these scopes, delete the file token.pickle.
from db import session
from models.historyPrice import HistoryPrice
from models.historyPromo import HistoryPromo
from models.mcityOffer import McityOffer
from models.Offer import Offer
from models.statsDaily import StatsDaily

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1lPFc1p_5TNSxYOtJ4hSqcSMAiUig4slRQTdMmgJroic'


def to_sheet(offers: List[Offer]):
    body = {'values': []}
    for o in offers:
        of_type = 'flat' if o.category == 'flat' else 'commercial'
        body['values'].append([
            '=HYPERLINK("https://www.cian.ru/{}/{}/{}";"{}")'.format(o.dealType, of_type, o.id, o.id),
            o.cianUserId,
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
            o.currency,
            o.paymentPeriod,
            o.floorNumber,
            str(o.totalArea),
            o.userTrust,
            o.isPro,
            o.publishTerms_autoprolong,
            o.prices[-1].price,
            o.promos[-1].services if o.promos else None,
            o.stats[-1].stats_total if o.stats else None,
            o.stats[-1].stats_daily if o.stats else None,
        ])
    return body


def to_mc_sheet(offers: List[McityOffer]):
    body = {'values': []}
    for o in offers:
        of_type = 'flat' if o.category == 'flat' else 'commercial'
        stats: StatsDaily = session.query(StatsDaily).order_by(StatsDaily.date.desc()).filter_by(id=o.id).first()
        body['values'].append([
            '=HYPERLINK("https://www.cian.ru/{}/{}/{}";"{}")'.format(o.dealType, of_type, o.id, o.id),
            '=HYPERLINK("https://www.mcity.ru/{}";"{}")'.format(o.idd, o.idd) if o.idd else None,
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
            o.currency,
            o.paymentPeriod,
            o.floorNumber,
            str(o.totalArea),
            o.userTrust,
            o.isPro,
            o.publishTerms_autoprolong,
            session.query(HistoryPrice).order_by(HistoryPrice.time.desc()).filter_by(id=o.id).first().price,
            session.query(HistoryPromo).order_by(HistoryPromo.date.desc()).filter_by(id=o.id).first().services,
            stats.stats_total if stats else None,
            stats.stats_daily if stats else None
        ])
    return body


def history(offers: List[Offer]):
    values = [['offer id', 'type', 'deal']]
    start_date = date(2019, 4, 26)
    dates = []
    for n in range((date.today() - start_date).days+1):
        dates.append(start_date + timedelta(n))
        values[0].append(dates[n].isoformat())

    for o in offers:
        row = [o.id, o.category, o.dealType]
        si = 0
        for cur_date in dates:
            sl = o.stats.__len__()
            nearest_date = o.stats[si].date if sl > si else None
            if nearest_date == cur_date:
                row.append(o.stats[si].stats_daily if o.stats[si].stats_daily is not None else '?')
                si += 1
            else:
                row.append(None)

        values.append(row)

    return {'values': values}


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

    td = (date.today() - date.fromisoformat('2019-04-27')).days

    mcityOffers = session.query(McityOffer).all()
    offers = session.query(Offer).all()

    # service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range='mcity!A2:W1000').execute()
    # service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range='all!A2:W5000').execute()
    service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range='dynamic!A1:W5000').execute()
    # result = service.spreadsheets().values().update(
    #     spreadsheetId=SPREADSHEET_ID, range='mcity!A2', valueInputOption='USER_ENTERED', body=to_mc_sheet(mcityOffers)
    # ).execute()
    # pprint(result)
    # result = service.spreadsheets().values().update(
    #     spreadsheetId=SPREADSHEET_ID, range='all!A2', valueInputOption='USER_ENTERED', body=to_sheet(offers)
    # ).execute()
    # pprint(result)

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='dynamic!A1',
        valueInputOption='USER_ENTERED',
        body=history(offers)
    ).execute()
    pprint(result)


if __name__ == '__main__':
    main()

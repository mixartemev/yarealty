import pickle
import os.path
from pprint import pprint
from typing import List
from datetime import date, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# If modifying these scopes, delete the file token.pickle.
from idna import unichr
from sqlalchemy import or_
from sqlalchemy.orm.collections import InstrumentedList

from db import session
from models.historyPrice import HistoryPrice
from models.historyPromo import HistoryPromo
from models.mcityOffer import McityOffer
from models.Offer import Offer
from models.statsDaily import StatsDaily
from models.phone import Phone
from models.user import User

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1lPFc1p_5TNSxYOtJ4hSqcSMAiUig4slRQTdMmgJroic'

PROMO_COLORS = {
    "top3": {"red": 0.65},
    "premium": {"green": 0.5},
    "paid": {"blue": 0.9}
}

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
sheets = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, fields='sheets.properties').execute()['sheets']


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
            o.prices[-1].price if o.prices else None,
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
        price: HistoryPrice = session.query(HistoryPrice).order_by(HistoryPrice.time.desc()).filter_by(id=o.id).first()
        promo = session.query(HistoryPromo).order_by(HistoryPromo.date.desc()).filter_by(id=o.id).first()
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
            price.price if price else None,
            promo.services if promo else None,
            stats.stats_total if stats else None,
            stats.stats_daily if stats else None
        ])
    return body


def history(offers: List[Offer]):
    values = [['offer id', 'user', 'last price', 'area', 'average']]
    start_date = date(2019, 7, 9)
    dates = []
    promo_data = []
    for n in range((date.today() - start_date).days + 1):
        dt = start_date + timedelta(n)
        if session.query(StatsDaily).filter_by(date=dt).count():
            dates.append(dt)
            values[0].append(dt.isoformat())

    for o in offers:
        of_type = 'flat' if o.category == 'flat' else 'commercial'
        row_num = values.__len__()+1
        row = [
            '=HYPERLINK("https://www.cian.ru/{}/{}/{}";"{}")'.format(o.dealType, of_type, o.id, o.id),
            '=HYPERLINK("https://www.cian.ru/company/{}";"{}")'.format(o.cianUserId, o.user.name if o.user else o.cianUserId),
            o.prices[-1].price if o.prices else None,
            int(o.totalArea),
            '=AVERAGE(F{}:{})'.format(row_num, row_num)
        ]
        promo_row_values = []
        si = 0
        for cur_date in dates:
            sl = o.stats.__len__()
            nearest_date = o.stats[si].date if sl > si else None
            if nearest_date == cur_date:
                row.append(o.stats[si].stats_daily if o.stats[si].stats_daily is not None else '?')
                promo: HistoryPromo = session.query(HistoryPromo)\
                    .filter(HistoryPromo.date <= cur_date.isoformat(), HistoryPromo.id == o.id)\
                    .order_by(HistoryPromo.date.desc())\
                    .first()

                promo_row_values.append(({"userEnteredFormat": {"textFormat": {
                            "foregroundColor": PROMO_COLORS[promo.services],
                            "bold": True
                        }}} if promo.services != 'free' else {}) if promo else {"userEnteredFormat": {"textFormat": {
                            "strikethrough": True
                        }}})
                si += 1
            else:
                row.append(None)
                promo_row_values.append({})

        if si:  # if row not empty
            values.append(row)
            promo_data.append({"values": promo_row_values})

    return [values, promo_data]


def columnToLetter(column):
    letter = ''
    while column > 0:
        temp = int((column - 1) % 26)
        letter = unichr(temp + 65) + letter
        column = (column - temp - 1) / 26
    return letter


def main():
    # # Create spreadsheet
    # spreadsheet = {'properties': {'title': 'MCity Cian Offers'}}
    # spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    # print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))

    rows = [
        ['id', 'name', 'creation date', 'is profi', 'is private broker', 'is moderated', 'status', 'account_type', 'phones']
    ]
    users = session.query(User).all()
    user: User
    for user in users:
        phones = list(map(lambda p: p.phone, user.phones))
        rows.append([
            user.id,
            user.name,
            user.creation_date.isoformat(),
            user.is_profi,
            user.is_private_broker,
            user.is_moderation_passed,
            user.status,
            user.account_type,
            ', '.join(phones)
        ])
    result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='users!A1',
            valueInputOption='RAW',
            body={'values': rows}
        ).execute()
    print(result)

    # service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range='mcity!A2:W1000').execute()
    # service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range='all!A2:W5000').execute()
    #
    # mcityOffers = session.query(McityOffer).all()
    offers = session.query(Offer)  # todo make entire monolit grouped sql query, escape from cycles

    # result = service.spreadsheets().values().update(
    #     spreadsheetId=SPREADSHEET_ID, range='mcity!A2', valueInputOption='USER_ENTERED', body=to_mc_sheet(mcityOffers)
    # ).execute()
    # pprint(result)
    # result = service.spreadsheets().values().update(
    #     spreadsheetId=SPREADSHEET_ID, range='all!A2', valueInputOption='USER_ENTERED', body=to_sheet(offers.all())
    # ).execute()
    # pprint(result)

    flatRent = offers.filter(
        or_(Offer.category == 'flat', Offer.category == 'newBuildingFlat'),
        Offer.dealType == 'rent'
    ).all()
    flatSale = offers.filter(or_(Offer.category == 'flat', Offer.category == 'newBuildingFlat'), Offer.dealType == 'sale').all()
    officeRent = offers.filter(or_(Offer.category == 'office', Offer.category == 'freeAppointmentObject'), Offer.dealType == 'rent').all()
    officeSale = offers.filter(or_(Offer.category == 'office', Offer.category == 'freeAppointmentObject'), Offer.dealType == 'sale').all()
    shopRent = offers.filter_by(category='shoppingArea', dealType='rent').all()
    shopSale = offers.filter_by(category='shoppingArea', dealType='sale').all()
    for sheet in sheets:
        sps = sheet['properties']
        if sps['title'].endswith('_stat'):
            rng = sps['title']+'!A1:'+columnToLetter(sps['gridProperties']['columnCount'])+str(sps['gridProperties']['rowCount'])
            service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=rng).execute()
            dyn(sps['sheetId'], sps['title'], locals()[sps['title'].replace('_stat', '')])


def dyn(dyn_sheet_id, dyn_sheet_title, offs: [Offer]):
    history_offers = history(offs)
    vals = history_offers[0]
    batch = 0
    while True:
        new_batch = batch+100
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=dyn_sheet_title+'!A'+str(batch+1),
            valueInputOption='USER_ENTERED',
            body={'values': vals[batch:new_batch]}
        ).execute()
        pprint(result)
        if vals.__len__() > new_batch:
            batch = new_batch
        else:
            break

    data_width = vals[0].__len__()
    fc = 5
    my_range = {
        'sheetId': dyn_sheet_id,
        'startRowIndex': 0,
        'endRowIndex': vals.__len__(),
        'startColumnIndex': 0,
        'endColumnIndex': data_width,
    }
    dates_range = {
        'sheetId': dyn_sheet_id,
        'startRowIndex': 0,
        'endRowIndex': 1,
        'startColumnIndex': fc,
        'endColumnIndex': data_width,
    }
    data_range = {
        'sheetId': dyn_sheet_id,
        'startRowIndex': 1,
        'endRowIndex': vals.__len__(),
        'startColumnIndex': fc,
        'endColumnIndex': data_width,
    }
    grad_range = {
        'sheetId': dyn_sheet_id,
        'startRowIndex': 1,
        'endRowIndex': vals.__len__(),
        'startColumnIndex': fc-1,
        'endColumnIndex': data_width,
    }
    info_range = {
        'sheetId': dyn_sheet_id,
        'startRowIndex': 0,
        'endRowIndex': vals.__len__(),
        'startColumnIndex': 0,
        'endColumnIndex': fc,
    }
    bold_border = {
        "style": "SOLID",
        "width": 2,
        "color": {},
    }
    norm_border = {
        "style": "SOLID",
        "width": 1,
        "color": {},
    }

    # clear_format = {'requests': [{"deleteConditionalFormatRule": {"sheetId": dyn_sheet_id}}]}
    # for i in range(5):
    #     response = service.spreadsheets() \
    #         .batchUpdate(spreadsheetId=SPREADSHEET_ID, body=clear_format).execute()
    #     print('{0} cells updated.'.format(len(response.get('replies'))))
    #     print(response)

    requests = [
        {
            "clearBasicFilter": {
                "sheetId": dyn_sheet_id
            }
        },
        {"updateCells": {
            "rows": history_offers[1],
            "range": data_range,
            "fields": 'userEnteredFormat'
        }},
        # drawing borders
        {
            "updateBorders": {
                "range": info_range,
                "right": bold_border,
                "innerHorizontal": norm_border,
                "innerVertical": norm_border
            }
        },
        {
            "updateBorders": {
                "range": my_range,
                "top": bold_border,
                "bottom": bold_border,
                "left": bold_border,
                "right": bold_border,
            }
        },
        # Froze header and left columns
        {
          "updateSheetProperties": {
            "properties": {
              "sheetId": dyn_sheet_id,
              "gridProperties": {
                "frozenColumnCount": fc,
                "frozenRowCount": 1,
              }
            },
            "fields": "gridProperties.frozenRowCount"
          }
        },
        # Date format
        {
            "repeatCell": {
                "range": {
                  "sheetId": dyn_sheet_id,
                  "startRowIndex": 0,
                  "endRowIndex": 1,
                  "startColumnIndex": fc,
                  "endColumnIndex": data_width
                },
                "cell": {
                  "userEnteredFormat": {
                    "numberFormat": {
                      "type": "DATE",
                      "pattern": "mm.dd"
                    }
                  }
                },
                "fields": "userEnteredFormat.numberFormat"
            }
        },
        # Auto width columns
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": dyn_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": fc,
                    "endIndex": data_width
                }
            }
        },
        # coloring weekends: saturday
        {
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [dates_range],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{
                                'userEnteredValue':
                                    '=EQ(WEEKDAY(INDIRECT(ADDRESS(1;COLUMN())));7)'
                            }]
                        },
                        'format': {
                            "backgroundColor": {'red': 0.957, 'green': 0.8, 'blue': 0.8},
                        }
                    }
                },
            }
        },
        # coloring weekends: sunday
        {
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [dates_range],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{
                                'userEnteredValue':
                                    '=EQ(WEEKDAY(INDIRECT(ADDRESS(1;COLUMN())));1)'
                            }]
                        },
                        'format': {
                            "backgroundColor": {'red': 0.92, 'green': 0.6, 'blue': 0.6},
                        }
                    }
                },
            }
        },
        # blackout empties
        {
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [data_range],
                    'booleanRule': {
                        'condition': {
                            'type': 'BLANK',
                        },
                        'format': {
                            "backgroundColor": {'red': 0},
                        }
                    }
                },
            }
        },
        # gray Nones
        {
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [data_range],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{"userEnteredValue": '?'}]
                        },
                        'format': {
                            "backgroundColor": {'red': 0.5, 'green': 0.5, 'blue': 0.5},
                        }
                    }
                },
            }
        },
        # coloring gradient
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [grad_range],
                    "gradientRule": {
                        "maxpoint": {
                            "color": {
                                "red": 1,
                                "green": 0.3,
                                "blue": 0.2
                            },
                            "type": "MAX"
                        },
                        "midpoint": {
                            "color": {
                                "red": 1,
                                "green": 1,
                                "blue": 0.2
                            },
                            "type": "PERCENT",
                            "value": '7'
                        },
                        "minpoint": {
                            "color": {
                                "red": 0.15,
                                "green": 0.9,
                                "blue": 1
                            },
                            "type": "MIN"
                        }
                    }
                }
            }
        },
    ]
    response = service.spreadsheets() \
        .batchUpdate(spreadsheetId=SPREADSHEET_ID, body={'requests': requests}).execute()
    print('{0} cells updated.'.format(len(response.get('replies'))))


if __name__ == '__main__':
    main()

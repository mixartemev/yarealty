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

PROMO_COLORS = {
    "top3": "red",
    "premium": "green",
    "paid": "blue"
}


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
    start_date = date(2019, 4, 25)
    dates = []
    promo_data = []
    for n in range((date.today() - start_date).days):
        dt = start_date + timedelta(n)
        if session.query(StatsDaily).filter_by(date=dt).count():
            dates.append(dt)
            values[0].append(dt.isoformat())

    for o in offers:
        of_type = 'flat' if o.category == 'flat' else 'commercial'
        row = ['=HYPERLINK("https://www.cian.ru/{}/{}/{}";"{}")'.format(o.dealType, of_type, o.id, o.id),
               o.category, o.dealType]
        promo_row_values = []
        si = 0
        for cur_date in dates:
            sl = o.stats.__len__()
            nearest_date = o.stats[si].date if sl > si else None
            if nearest_date == cur_date:
                row.append(o.stats[si].stats_daily if o.stats[si].stats_daily is not None else '?')
                promo: HistoryPromo = session.query(HistoryPromo)\
                    .filter(HistoryPromo.date <= cur_date.isoformat())\
                    .order_by(HistoryPromo.date.desc())\
                    .first()

                promo_row_values.append({"userEnteredFormat": {"borders": {"bottom": {
                            "style": "SOLID",
                            "width": 3,
                            "color": {PROMO_COLORS[promo.services]: 1},
                        }}}})
                si += 1
            else:
                row.append(None)
                promo_row_values.append({})

        values.append(row)
        promo_data.append({"values": promo_row_values})

    return [{'values': values}, promo_data]


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
    # todo from stats
    offers = session.query(Offer).all()  # .limit(100)

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

    history_offers = history(offers)
    cells_data = history_offers[0]
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='dynamic!A1',
        valueInputOption='USER_ENTERED',
        body=cells_data
    ).execute()
    pprint(result)

    vals = cells_data.get('values')
    dyn_sheet_id = 656058326
    data_width = vals[0].__len__()
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
        'startColumnIndex': 3,
        'endColumnIndex': data_width,
    }
    data_range = {
        'sheetId': dyn_sheet_id,
        'startRowIndex': 1,
        'endRowIndex': vals.__len__(),
        'startColumnIndex': 3,
        'endColumnIndex': data_width,
    }
    info_range = {
        'sheetId': dyn_sheet_id,
        'startRowIndex': 0,
        'endRowIndex': vals.__len__(),
        'startColumnIndex': 0,
        'endColumnIndex': 3,
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

    requests = [
        {"updateCells": {
            "rows": history_offers[1],
            "range": data_range,
            "fields": 'userEnteredFormat'
        }},
        # {
        #     "updateCells": {
        #         "rows": [
        #             {  # object(GridData)
        #                 "values": [
        #                     {
        #                         "userEnteredValue": {  # object(ExtendedValue)
        #                             # "numberValue": 11,
        #                             "stringValue": 'string',
        #                             # "boolValue": boolean,
        #                             # "formulaValue": string,
        #                             # "errorValue": {
        #                             #   "type": enum(ErrorType),
        #                             #   "message": string
        #                             # }
        #                         },
        #                         # "effectiveValue": { # This field is read-only.
        #                         #     object(ExtendedValue)
        #                         # },
        #                         # "formattedValue": string, # This field is read-only.
        #                         "userEnteredFormat": {
        #                             "backgroundColor": {"red": 0.5},
        #                             # "numberFormat": {
        #                             #   object(NumberFormat)
        #                             # },
        #                             # "borders": {
        #                             #   object(Borders)
        #                             # },
        #                             # "padding": {
        #                             #   object(Padding)
        #                             # },
        #                             # "horizontalAlignment": enum(HorizontalAlign),
        #                             # "verticalAlignment": enum(VerticalAlign),
        #                             # "wrapStrategy": enum(WrapStrategy),
        #                             # "textDirection": enum(TextDirection),
        #                             # "textFormat": {
        #                             #   object(TextFormat)
        #                             # },
        #                             "hyperlinkDisplayType": 'LINKED',
        #                             # "textRotation": {
        #                             #   object(TextRotation)
        #                             # }
        #                         },
        #                         # "effectiveFormat": { # This field is read-only.
        #                         #     object(CellFormat)
        #                         # },
        #                         # "hyperlink": 'ya.ru', # This field is read-only.
        #                         "textFormatRuns": [
        #                             {
        #                                 "startIndex": 0,
        #                                 "format": {
        #                                     "foregroundColor": {"blue": 0.5},
        #                                     "bold": True,
        #                                     "italic": True,
        #                                     "strikethrough": False,
        #                                     # "underline": True
        #                                 }
        #                             }
        #                         ],
        #                         # "dataValidation": {
        #                         #     object(DataValidationRule)
        #                         # },
        #                         # "pivotTable": {
        #                         #     object(PivotTable)
        #                         # }
        #                     }
        #                 ]
        #             }
        #         ],
        #         "fields": '*',
        #         "range": my_range
        #     },
        # },

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
                "frozenColumnCount": 3,
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
                  "startColumnIndex": 3,
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
                    "startIndex": 3,
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
                            "backgroundColor": {'red': 0.4, 'green': 0.4, 'blue': 0.4},
                        }
                    }
                },
            }
        },
        # coloring gradient
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [data_range],
                    "gradientRule": {
                        "maxpoint": {
                            "color": {
                                "red": 0.945,
                                "green": 0.153,
                                "blue": 0.067
                            },
                            "type": "MAX"
                        },
                        "midpoint": {
                            "color": {
                                "red": 1,
                                "green": 1,
                                "blue": 0.1
                            },
                            "type": "PERCENT",
                            "value": '7'
                        },
                        "minpoint": {
                            "color": {
                                "red": 0,
                                "green": 0.7647,
                                "blue": 1
                            },
                            "type": "MIN"
                        }
                    }
                }
            }
        },
    ]
    body = {
        'requests': requests
    }

    clear_format = {'requests': [{"deleteConditionalFormatRule": {"sheetId": dyn_sheet_id}}]}
    for i in range(5):
        response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=SPREADSHEET_ID, body=clear_format).execute()
        print('{0} cells updated.'.format(len(response.get('replies'))))
        print(response)

    response = service.spreadsheets() \
        .batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(len(response.get('replies'))))


if __name__ == '__main__':
    main()

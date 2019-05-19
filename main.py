import argparse
import requests
import time
from datetime import date
from random import randint
from models.statsDaily import StatsDaily
from models.historyPrice import HistoryPrice
from models.historyPromo import HistoryPromo
from models.mcityOffer import McityOffer
from models.Offer import Offer
from db import session
from req import make as make_request
from converter import convert
# from models.bc import Bc
# from models.house import House
# from models.location import Location
# from models.newbuilding import Newbuilding
# import csv
#
# with open('temp/locations.tsv') as tsvfile:
#     reader = csv.reader(tsvfile, delimiter='\t')
#     for row in reader:
#         params = tuple(row)
#         session.merge(Location(*params))
#
# with open('temp/newbuildings.tsv') as tsvfile:
#     reader = csv.reader(tsvfile, delimiter='\t')
#     for row in reader:
#         params = tuple(row)
#         session.merge(Newbuilding(*params))
#
# with open('temp/houses.tsv') as tsvfile:
#     reader = csv.reader(tsvfile, delimiter='\t')
#     for row in reader:
#         params = tuple(row)
#         session.merge(House(*params))
#
# with open('temp/bc.tsv') as tsvfile:
#     reader = csv.reader(tsvfile, delimiter='\t')
#     for row in reader:
#         if row[3]:
#             if not session.query(Bc).get(row[3]):
#                 continue
#         params = tuple(row)
#         session.merge(Bc(*params))
# session.commit()


def upd_stats():
    o: Offer
    for o in session.query(Offer).all():
        for i, s in enumerate(o.stats):
            if s.stats_daily is None:
                if i > 0 and o.stats[i-1].stats_total is not None and o.stats[i-1].stats_daily is not None:
                    s.stats_total = o.stats[i-1].stats_total + o.stats[i-1].stats_daily
                if (i+1) < o.stats.__len__() and o.stats[i+1].stats_total is not None and s.stats_total is not None:
                    s.stats_daily = o.stats[i+1].stats_total - s.stats_total
                session.commit()


def main():
    # upd_stats()
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_id', type=int, default=None, help='user id')
    parser.add_argument('--bs_center_id', type=int, default=8366, help='bs_center id')
    parser.add_argument('--start_page', type=int, default=1, help='page number to start')
    args = parser.parse_args()

    try:
        for offer_type in ['office', 'flat']:
            for deal_type in ['rent', 'sale']:
                print(offer_type, deal_type)
                current_page = 1
                while True:
                    print("Processing page {}...".format(current_page))

                    result = make_request(args, offer_type, deal_type, current_page)

                    if 'error' in result:
                        exit()

                    res: list = result['data']['offers']
                    mc_count = 0
                    ok = True

                    for e in convert(res):
                        if e['offer'][9] != 'dailyFlat':
                            offer: Offer = session.query(Offer).get(e['offer'][0])
                            session.merge(Offer(*e['offer']))

                            stats_exists = offer and offer.stats and offer.stats[-1].date == date.today()
                            if e['statsDaily'][1] is None or e['statsDaily'][1] is None:
                                print(offer_type, deal_type, current_page, 'Stats None')
                                ok = False
                                time.sleep(3)
                                break
                            if not stats_exists:
                                session.merge(StatsDaily(*e['statsDaily']))
                            elif stats_exists and (offer.stats[-1].stats_daily is None or offer.stats[-1].stats_daily <
                                                   e['statsDaily'][2]):  # and e['statsDaily'][2] is not None
                                session.query(StatsDaily) \
                                    .filter_by(id=e['statsDaily'][0], date=date.today()) \
                                    .update({"stats_total": e['statsDaily'][1], "stats_daily": e['statsDaily'][2]})

                            if e['offer'][1] == 9383110:
                                mc_count += 1
                                session.merge(McityOffer(*e['mcityOffer']))

                            hp = e['historyPromo']
                            if offer and not offer.promos:
                                print("Obj {} hasn't prices?".format(offer.id))
                            if not (offer and offer.promos and offer.promos[-1].services == hp[1]):
                                session.add(HistoryPromo(*hp))

                            if e['historyPrice'] is None:
                                print(offer_type, deal_type, current_page, 'Price None')
                                continue
                            for p in e['historyPrice']:
                                h = HistoryPrice(*p)
                                c = session.query(HistoryPrice).filter_by(id=h.id, time=h.time).count()
                                if not c:
                                    session.merge(h)

                    if ok:
                        session.commit()
                        current_page += 1
                        delay = randint(3, 10)
                        length = res.__len__()
                        print("{0} {1} {2} (inc {3} mcity) received.\nWaiting {4} seconds..".format(
                            length, deal_type, offer_type, mc_count, delay
                        ))
                        time.sleep(delay)
                        if length < 50:
                            break  # Объявлений больше нет -> съёбки

    except Exception as e:
        print(e)
        print("Unknown exception.. Push: {}".format(push(False)))
        exit()
    except KeyboardInterrupt:
        print("Finishing...")
        exit()
    print("Done. Push: {}".format(push()))


def push(ok=True):
    url = 'https://fcm.googleapis.com/fcm/send'
    title = 'Мегапарсёр отработал'
    mess = 'Данные успешно спизджены полностью' if ok else 'Пизда рулю. Все сломалось'
    act = 'https://docs.google.com/spreadsheets/d/1lPFc1p_5TNSxYOtJ4hSqcSMAiUig4slRQTdMmgJroic/edit#gid=656058326'
    tok = 'cDBL0-jYBWQ:APA91bG294ZcB0TkztsUkt-hBayeC6kPnYBzY6swFSEgNtJGdB5ht1xm-Kq_7VokWMLH35ecV9SbR0PMm7qrxmXtTO8tPkNUJ09F1j2m0B923BYrh8mOzQGubb3xdNHR249mvwrWM-fb'
    body = {
      "notification": {
        "title": title,
        "body": mess + ' ' + date.today().isoformat(),
        "icon": "https://avatars1.githubusercontent.com/u/5181924?s=460&v=4",
        "topic": "excel",
        "click_action": act
      },
      "to": tok
    }
    headers = {
        "Authorization": "key=AAAAdDA0FEM:APA91bGovsJXVAm0R3P5DNBZsWbvwbXacLmjvlDst2t3o8VNWUhJ63UUgNeZfcTZXuWQw9LWPHGJt5dn20hDBEDt-cjmw91i_ncfg9qE5eqifRNULeEbMPQgMRUpLw4yZrUCyeluO2TZ",
        "Content-Type": "application/json"
    }
    return requests.post(url, json=body, headers=headers).status_code


if __name__ == '__main__':
    main()

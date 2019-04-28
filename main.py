import argparse
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


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--deal_type', type=str, default="rent", help='realty type')
    parser.add_argument('--offer_type', type=str, default="office", help='realty category')
    parser.add_argument('--user_id', type=int, default=None, help='user id')
    parser.add_argument('--bs_center_id', type=int, default=8366, help='bs_center id')
    parser.add_argument('--start_page', type=int, default=1, help='page number to start')
    args = parser.parse_args()
    current_page = args.start_page

    try:
        while True:
            print("Processing page {}...".format(current_page))

            result = make_request(args, current_page)

            if 'error' in result:
                exit()

            res: list = result['data']['offers']
            mc_count = 0

            for e in convert(res):
                if e['offer'][9] != 'dailyFlat':
                    if e['offer'][1] == 9383110:
                        mc_count += 1
                        session.merge(McityOffer(*e['mcityOffer']))
                    offer: Offer = session.query(Offer).get(e['offer'][0])
                    session.merge(Offer(*e['offer']))

                    hp = e['historyPromo']
                    if offer and not offer.promos:
                        print("Obj {} hasn't prices?".format(offer.id))
                    if not(offer and offer.promos and offer.promos[-1].services == hp[1]):
                        session.add(HistoryPromo(*hp))

                    for p in e['historyPrice']:
                        h = HistoryPrice(*p)
                        c = session.query(HistoryPrice).filter_by(id=h.id, time=h.time).count()
                        if not c:
                            session.merge(h)

                    stats_exists = offer and offer.stats[-1].date == date.today()
                    if not stats_exists:
                        session.merge(StatsDaily(*e['statsDaily']))
                    elif stats_exists and offer.stats[-1].stats_daily < e['statsDaily'][2]:
                        session.query(StatsDaily)\
                            .filter_by(id=e['statsDaily'][0], date=date.today())\
                            .update({"stats_total": e['statsDaily'][1], "stats_daily": e['statsDaily'][2]})

            session.commit()

            current_page += 1
            delay = randint(5, 20)
            length = res.__len__()
            print("{0} {1} {2} (inc {3} mcity) received.\nWaiting {4} seconds..".format(
                length, args.deal_type, args.offer_type, mc_count, delay
            ))
            if length < 50:
                break  # Объявлений больше нет -> съёбки
            time.sleep(delay)
    except Exception as e:
        print(e)
        print("Unknown exception, waiting 60 seconds.")
        time.sleep(60)
    except KeyboardInterrupt:
        print("Finishing...")
        exit()
    print("Done")


if __name__ == '__main__':
    main()

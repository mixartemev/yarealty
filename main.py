# from models.bc import Bc
# from models.house import House
# from models.location import Location
# from models.newbuilding import Newbuilding
import argparse
import time
from random import randint
from models.offer import Offer
from models.rivalOffer import RivalOffer
from db import session
from req import make as make_request
from converter import convert

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
    parser.add_argument('--user_id', type=int, default=9383110, help='user id')
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

            if not res:
                break  # Объявлений больше нет -> съёбки

            for e in convert(res):
                session.merge(Offer(*e['Offer']) if args.user_id == 9383110 else RivalOffer(*e['rivalOffer']))

            session.commit()
            current_page += 1
            delay = randint(5, 15)
            print("{0} {1} {2} {3} received.\nWaiting {4} seconds.."
                  .format(res.__len__(), args.deal_type, args.offer_type, 'mcities' if args.user_id == 9383110 else 'rivals', delay))
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

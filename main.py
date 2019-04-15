from models.bc import Bc
from models.house import House
from models.location import Location
from models.newbuilding import Newbuilding
from models.offer import Offer
from db import session
from req import arguments as args, make as make_request
from converter import convert
import time

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

# with open('temp/bc_id.tsv') as tsvfile:
#     reader = csv.reader(tsvfile, delimiter='\t')
#     for row in reader:
#         if row[3]:
#             if not session.query(Bc).get(row[3]):
#                 continue
#         params = tuple(row)
#         session.merge(Bc(*params))


def main():
    current_page = args.page_number
    try:
        print("Processing page {}...".format(current_page))
        result = make_request(args, current_page)

        if 'error' in result:
            exit()

        res = result['data']['offers']

        for e in convert(res):
            session.merge(Offer(*e['offer']))

        session.commit()
        current_page += 1
        print("Waiting {0} seconds".format(args.delay))
        time.sleep(args.delay)
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

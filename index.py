from models.site import Site
from models.building import Building
from models.offer import Offer
from db import session
from req import arguments as args, make as make_request
from converter import convert
import time


def main():
    current_page = args.page_number
    try:
        print("Processing page {}...".format(current_page))
        result = make_request(args, current_page)

        if 'error' in result:
            exit()

        res = result['response']['search']['offers']['entities']
        # res = list(filter(lambda r: r['building'].get('buildingId'), res))
        for e in convert(res):
            if e['site']:
                session.merge(Site(*e['site']))
            b = session.merge(Building(*e['building']))
            session.commit()
            o = (b.id,) + e['offer']
            session.merge(Offer(*o))
            # session.merge(Photo(*e['photo']))
        # for ent in res:
        #     session.merge(Offer(
        #         ent['offerId'],
        #         ent['active'],
        #         ent['area']['value'],
        #         ent['building'].get('houseId')
        #     ))

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

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

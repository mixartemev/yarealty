import argparse
import time
import requests

from converter import convert_building
from models import session, Offer

API_URL = "https://realty.yandex.ru/gate/react-page/get/?rgid={0}&type={1}&category={2}&page={3}&_format=react" \
          "&_pageType=search&_providers=react-search-data&pageSize=2"  # &searchType=newbuilding-search


def read_cookies():
    with open("./cookies.txt", encoding='utf-8', newline="\n") as f:
        return {cookie.split(" ", 2)[0]: cookie.split(" ", 2)[1].replace('\n', '') for cookie in f}


def make_request(args, page_number) -> dict:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "realty.yandex.ru",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
    }
    cookies = read_cookies()

    url = API_URL.format(args.rgid, args.type, args.category, page_number)
    r = requests.get(url, headers=headers, cookies=cookies)
    return r.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_file', type=str, default='output/output.json', help='directory to save parsed data')
    parser.add_argument('--page_number', type=int, default=1, help='page number to start')
    parser.add_argument('--delay', type=float, default=3, help='delay between requests')
    parser.add_argument('--rgid', type=int, default=187, help='region id')
    parser.add_argument('--type', type=str, default="SELL", help='realty type')
    parser.add_argument('--category', type=str, default="APARTMENT", help='realty category')
    args = parser.parse_args()
    current_page = args.page_number
    try:
        print("Processing page {}...".format(current_page))
        result = make_request(args, current_page)

        if 'error' in result:
            exit()

        res = result['response']['search']['offers']['entities']

        session.merge(convert_building(res))
        for ent in res:
            session.merge(Offer(
                ent['offerId'],
                ent['active'],
                ent['area']['value'],
                ent['building'].get('houseId')
            ))

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

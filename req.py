import argparse
import requests

API_URL = "https://realty.yandex.ru/gate/react-page/get/?rgid={0}&type={1}&category={2}&page={3}&_format=react" \
          "&_pageType=search&_providers=react-search-data&pageSize=237"  # &searchType=newbuilding-search

parser = argparse.ArgumentParser()
parser.add_argument('--output_file', type=str, default='output/output.json', help='directory to save parsed data')
parser.add_argument('--page_number', type=int, default=1, help='page number to start')
parser.add_argument('--delay', type=float, default=3, help='delay between requests')
parser.add_argument('--rgid', type=int, default=187, help='region id')
parser.add_argument('--type', type=str, default="SELL", help='realty type')
parser.add_argument('--category', type=str, default="APARTMENT", help='realty category')
arguments = parser.parse_args()


def _read_cookies() -> dict:
    with open("./cookies.txt", encoding='utf-8', newline="\n") as f:
        return {cookie.split(" ", 2)[0]: cookie.split(" ", 2)[1].replace('\n', '') for cookie in f}


def make(args, page_number: int) -> dict:
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
    cookies = _read_cookies()

    url = API_URL.format(args.rgid, args.type, args.category, page_number)
    r = requests.get(url, headers=headers, cookies=cookies)
    return r.json()

import argparse
import requests

API_URL = "http://api.cian.ru/search-offers/v1/search-offers-for-mobile-apps/?deal_type={0}&offer_type={1}&id_user={2}"\
          "&p={3}&engine_version=2&new_schema=1&per_page=50"

parser = argparse.ArgumentParser()
parser.add_argument('--deal_type', type=str, default="rent", help='realty type')
parser.add_argument('--offer_type', type=str, default="office", help='realty category')
parser.add_argument('--id_user', type=int, default=9383110, help='user id')
parser.add_argument('--page_number', type=int, default=0, help='page number to start')
parser.add_argument('--delay', type=float, default=3, help='delay between requests')
arguments = parser.parse_args()


def _read_cookies() -> dict:
    with open("./cookies.txt", encoding='utf-8', newline="\n") as f:
        return {cookie.split(" ", 2)[0]: cookie.split(" ", 2)[1].replace('\n', '') for cookie in f}


def make(args, page_number: int) -> dict:
    headers = {
        "Accept": "*/*",
        "Authorization": "simple eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM3NDMxOTA5LWQ3OWQtNGUwMy04OGRjLWE3ODRkYzZjMDE5YyIsImlzUmVnaXN0ZXJlZCI6ZmFsc2V9.MbZKw7_e6ZZiUdzPTPohzWahEnIZQAfvkxPZGoTs4j4",
        "ApplicationID": "7B8669C8-E0CF-4F4E-AE15-70A1B0606D9F",
        "User-Agent": "CIAN/1.84 (iPhone; iOS 12.2; Scale/3.00; 7B8669C8-E0CF-4F4E-AE15-70A1B0606D9F)",
    }
    cookies = _read_cookies()

    url = API_URL.format(args.deal_type, args.offer_type, args.id_user, page_number)
    r = requests.get(url, headers=headers, cookies=cookies)
    return r.json()

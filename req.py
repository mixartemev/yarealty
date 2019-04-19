import requests

COMMON_URL = "http://api.cian.ru/search-offers/v1/search-offers-for-mobile-apps/" \
          "?deal_type={0}&offer_type={1}&p={2}&engine_version=2&new_schema=1&per_page=50"

API_MCITY_URL = COMMON_URL + "&id_user={3}"
API_OFFICE_URL = COMMON_URL + "&bs_center_id={3}"
API_FLAT_URL = COMMON_URL + "&newobject[0]=1502&newobject[1]=5222&newobject[2]=5227&newobject[3]=5340&newobject[4]=" \
                            "5386&newobject[5]=5822&newobject[6]=6322&newobject[7]=8825&newobject[8]=45865"


def _read_cookies() -> dict:
    with open("./cookies.txt", encoding='utf-8', newline="\n") as f:
        return {cookie.split(" ", 2)[0]: cookie.split(" ", 2)[1].replace('\n', '') for cookie in f}


def make(args, page_number: int) -> dict:
    headers = {
        "Accept": "*/*",
        "Authorization": "simple eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM3NDMxOTA5LWQ3OWQtNGUwMy04OGRjLWE3"
                         "ODRkYzZjMDE5YyIsImlzUmVnaXN0ZXJlZCI6ZmFsc2V9.MbZKw7_e6ZZiUdzPTPohzWahEnIZQAfvkxPZGoTs4j4",
        # "ApplicationID": "7B8669C8-E0CF-4F4E-AE15-70A1B0606D9F",
        # "User-Agent": "CIAN/1.84 (iPhone; iOS 12.2; Scale/3.00; 7B8669C8-E0CF-4F4E-AE15-70A1B0606D9F)",
    }
    cookies = _read_cookies()

    third = args.user_id if args.user_id else args.bs_center_id
    url = API_FLAT_URL.format(args.deal_type, args.offer_type, page_number)
    r = requests.get(url, headers=headers, cookies=cookies)
    return r.json()

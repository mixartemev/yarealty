import re
from typing import List, Tuple


def convert(raw_data: list):
    for e in raw_data:
        yield {
            "offer": _offer(e),
            "mcityOffer": _mcityOffer(e),
            "statsDaily": _statsDaily(e),
            "historyPrice": _historyPrice(e),
            "historyPromo": _historyPromo(e),
        }


def _mcityOffer(o: dict) -> tuple:
    idd = re.match(r'ID:(\d{6})', o['description'])
    return (
        o['id'],
        idd.groups()[0] if idd else None,
        o['businessShoppingCenter'].get('id') if o.get('businessShoppingCenter') else None,
        o['newbuilding']['house']['id'] if (o['newbuilding'].get('house') if o.get('newbuilding') else None) else None,
        o['newbuilding']['id'] if o.get('newbuilding') else None,
        o['description'],
        o['creationDate'],
        o['editDate'],
        o['publishDate'],
        o['category'].replace(o['dealType'].title(), ''),
        o['dealType'],
        o['status'],
        o['bargainTerms']['currency'],
        o['bargainTerms'].get('paymentPeriod'),
        o.get('floorNumber'),
        o['totalArea'],
        o['userTrust'],
        o.get('isPro'),
        o['publishTerms'].get('autoprolong'),
    )


def _offer(o: dict) -> tuple:
    return (
        o['id'],
        o['cianUserId'],
        o['businessShoppingCenter'].get('id') if o.get('businessShoppingCenter') else None,
        o['newbuilding']['house']['id'] if (o['newbuilding'].get('house') if o.get('newbuilding') else None) else None,
        o['newbuilding']['id'] if o.get('newbuilding') else None,
        o['description'],
        o['creationDate'],
        o['editDate'],
        o['publishDate'],
        o['category'].replace(o['dealType'].title(), ''),
        o['dealType'],
        o['status'],
        o['bargainTerms']['currency'],
        o['bargainTerms'].get('paymentPeriod'),
        o.get('floorNumber'),
        o['totalArea'],
        o['userTrust'],
        o.get('isPro'),
        o['publishTerms'].get('autoprolong'),
        o['bargainTerms'].get('priceType'),
        o.get('minArea'),
    )


def _statsDaily(o: dict) -> Tuple[int, int, int]:
    return (
        o['id'],
        o['stats']['total'] if o.get('stats') else None,
        o['stats']['daily'] if o.get('stats') else None,
    )


def _historyPromo(o: dict) -> Tuple[int, str]:
    return (
        o['id'],
        o['services'][0]
    )


def _historyPrice(o: dict) -> List[Tuple[int, float, int]] or None:
    prices = []
    if not o.get('historyPriceChanges'):
        print("Obj {} hasn't prices!".format(o['id']))
        return None
    for ph in o['historyPriceChanges']:
        prices.append((o['id'], ph["changeTime"], ph["priceData"]["price"]))
    return prices

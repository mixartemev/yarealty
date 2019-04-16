import re


def convert(raw_data: list):
    for e in raw_data:
        yield {
            "offer": _offer(e),
        }


def _offer(o: dict) -> tuple:
    idd = re.match(r'ID:(\d{6})', o['description']).groups()[0]
    return (
        o['id'],
        idd,
        o['businessShoppingCenter'].get('id') if o.get('businessShoppingCenter') else None,
        o['newbuilding']['house']['id'] if (o['newbuilding'].get('house') if o.get('newbuilding') else None) else None,
        o['newbuilding']['id'] if o.get('newbuilding') else None,
        o['description'],
        o['creationDate'],
        o['editDate'],
        o['publishDate'],
        # o['offerType'],
        o['category'].replace(o['dealType'].title(), ''),
        o['dealType'],
        o['status'],
        o['bargainTerms']['currency'],
        o['bargainTerms']['price'],
        o['pricePerUnitArea'] if o.get('pricePerUnitArea') else None,
        o['floorNumber'],
        o['totalArea'],
        o['services'][0],
        o['userTrust'],
        o['isPro'],
        o['stats']['total'] if o.get('stats') else None,
        o['stats']['daily'] if o.get('stats') else None,
        o['publishTerms'].get('autoprolong'),
    )

import re


def convert(raw_data: list):
    for e in raw_data:
        yield {
            "offer": _offer(e),
            "rivalOffer": _rivalOffer(e),
        }


def _offer(o: dict) -> tuple:
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
        o['bargainTerms']['price'],
        o['pricePerUnitArea'] if o.get('pricePerUnitArea') else None,
        o['floorNumber'],
        o['totalArea'],
        o['services'][0],
        o['userTrust'],
        o.get('isPro'),
        o['stats']['total'] if o.get('stats') else None,
        o['stats']['daily'] if o.get('stats') else None,
        o['publishTerms'].get('autoprolong'),
    )


def _rivalOffer(o: dict) -> tuple:
    return (
        o['id'],
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
        o['bargainTerms']['price'],
        o['pricePerUnitArea'] if o.get('pricePerUnitArea') else None,
        o['floorNumber'],
        o['totalArea'],
        o['services'][0],
        o['userTrust'],
        o.get('isPro'),
        o['stats']['total'] if o.get('stats') else None,
        o['stats']['daily'] if o.get('stats') else None,
        o['publishTerms'].get('autoprolong'),
    )

def convert(raw_data: list):
    for e in raw_data:
        yield {
            "offer": _offer(e),
        }


def _offer(o: dict) -> tuple:
    return (
        o['id'],
        o['businessShoppingCenter'].get('id'),
        o['newbuilding']['id'] if o.get('newbuilding') else None,
        o['description'],
        o['creationDate'],
        o['editDate'],
        o['publishDate'],
        o['offerType'],
        o['dealType'],
        o['status'],
        o['bargainTerms']['currency'],
        o['priceTotalPerMonth'],
        o['pricePerUnitArea'],
        o['floorNumber'],
        o['totalArea'],
        o['services'][0],
        o['userTrust'],
        o['isPro'],
        o['publishTerms'].get('autoprolong'),
    )

def try_extract_value(dic, path):
    keys = path.split(".")
    dv = dic
    for key in keys:
        if key not in dv:
            return None
        dv = dv[key]
    return dv


def convert(raw_data: list):
    for e in raw_data:
        yield {
            "author": _author(e),
            "site": _site(e['building']),
            "building": _building(e),
            "offer": _offer(e),
            # "photo": _photo(e)
        }


def _site(s: dict) -> tuple:
    return (
        s['siteId'],  # id
        s['siteName'],
        s['siteDisplayName']
    ) if s.get('siteId') else None


def _building(o: dict) -> tuple:
    b = o['building']
    return (
        b.get('buildingId'),  # id
        b.get('builtYear'),
        b.get('builtQuarter'),
        b.get('buildingState'),
        b.get('buildingType'),
        b.get('siteId'),
        b.get('houseId'),
        o['floorsTotal'],
        # 'improvements': {'LIFT': True,
        # 'RUBBISH_CHUTE': True,
        # 'SECURITY': True},
        # 'heatingType': 'UNKNOWN',
    )


def _author(o: dict) -> tuple:
    a = o['author']
    return (
        o.get('partnerId'),
        o.get('partnerInternalId'),
        o.get('partnerName'),
        a.get('agentName'),
        a.get('category'),
        a['encryptedPhones'][0],
        a['encryptedPhoneNumbers'][0]['redirectId'] if a['redirectPhones'] else None,
    )


def _offer(o: dict) -> tuple:
    extract = try_extract_value

    if extract(o, "price.unitPerPart") == "SQUARE_METER":
        price_m2 = extract(o, "price.valuePerPart")
    else:
        price_m2 = None

    floors_offered = extract(o, "floorsOffered")
    if type(floors_offered) is list and len(floors_offered) > 0:
        floor = floors_offered[0]
    else:
        floor = None

    return (
        o['offerId'],
        o['trust'],
        o['active'],
        o.get('roomsTotal'),
        extract(o, "price.value"),
        price_m2,
        floor,
        o['area']['value'],
        extract(o, "livingSpace.value"),
        extract(o, "roomSpace.value"),
        extract(o, "kitchenSpace.value"),
        extract(o, "partnerId"),
        o['creationDate'],
        o['description'],
        # o['offerType'],
        # o['description'],
        # # extract(o, 'appLargeImages'),
        # extract(o, "apartment.renovation"),
        # extract(o, "house.bathroomUnit"),
        # extract(o, "house.windowView"),
        # extract(o, "apartment.improvements.NO_FURNITURE") is True,
        # extract(o, "ceilingHeight"),
        # 1 if extract(o, "house.balconyType") is not None else 0,
    )


def _photo(b: dict) -> tuple:
    return (
        b['buildingId'],  # id
        b['builtYear'],
        b.get('builtQuarter'),
        b.get('siteId')
        # 'buildingState': 'UNFINISHED',
        # 'buildingType': 'MONOLIT',
        # 'improvements': {'LIFT': True,
        # 'RUBBISH_CHUTE': True,
        # 'SECURITY': True},
        # 'siteId': 194000,
        # 'siteName': 'Green park',
        # 'siteDisplayName': 'Жилой район Green park',
        # 'houseId': '843164',
        # 'heatingType': 'UNKNOWN',
        # 'buildingImprovementsMap': {'LIFT': True,
        # 'RUBBISH_CHUTE': True,
        # 'SECURITY': True,
    )

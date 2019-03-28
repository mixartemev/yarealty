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
            "site": _site(e['building']),
            "building": _building(e['building']),
            # "offer": _offer(e),
            # "photo": _photo(e)
        }


def _site(s: dict) -> tuple:
    return (
        s['siteId'],  # id
        s['siteName'],
        s['siteDisplayName']
    ) if s.get('siteId') else None


def _building(b: dict) -> tuple:
    return (
        b.get('buildingId'),  # id
        b.get('builtYear'),
        b.get('builtQuarter'),
        b.get('buildingState'),
        b.get('buildingType'),
        b.get('siteId'),
        b.get('houseId'),
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

    yield (
        o['offerId'],
        o['active'],
        o['roomsTotal'],
        price_m2,
        floor,
        o['area']['value'],
        extract(o, "livingSpace.value"),
        extract(o, "roomSpace.value"),
        extract(o, "kitchenSpace.value"),
        extract(o, "building.houseId"),
        extract(o, "building.siteId"),
        extract(o, "author.id"),
        extract(o, "price.value"),
        o['creationDate'],
        o['offerType'],
        o['description'],
        # extract(o, 'appLargeImages'),
        extract(o, "apartment.renovation"),
        extract(o, "house.bathroomUnit"),
        extract(o, "house.windowView"),
        extract(o, "apartment.improvements.NO_FURNITURE") is True,
        extract(o, "ceilingHeight"),
        1 if extract(o, "house.balconyType") is not None else 0,
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

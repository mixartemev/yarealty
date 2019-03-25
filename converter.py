def try_extract_value(dic, path):
    keys = path.split(".")
    dv = dic
    for key in keys:
        if key not in dv:
            return None
        dv = dv[key]
    return dv


def convert_offer(raw_data):
    extract = try_extract_value
    for e in raw_data:

        if extract(e, "price.unitPerPart") == "SQUARE_METER":
            price_m2 = extract(e, "price.valuePerPart")
        else:
            price_m2 = None

        floors_offered = extract(e, "floorsOffered")
        if type(floors_offered) is list and len(floors_offered) > 0:
            floor = floors_offered[0]
        else:
            floor = None

        yield (
            e['offerId'],
            e['active'],
            e['roomsTotal'],

            floor,
            e['area']['value'],
            extract(e, "livingSpace.value"),
            extract(e, "roomSpace.value"),
            extract(e, "kitchenSpace.value"),
            extract(e, "building.houseId"),
            extract(e, "building.siteId"),
            extract(e, "author.id"),
            extract(e, "price.value"),
            e['creationDate'],
            e['offerType'],
            e['description'],
            # extract(e, 'appLargeImages'),
            extract(e, "apartment.renovation"),
            extract(e, "house.bathroomUnit"),
            extract(e, "house.windowView"),
            extract(e, "apartment.improvements.NO_FURNITURE") is True,
            extract(e, "ceilingHeight"),
            1 if extract(e, "house.balconyType") is not None else 0,
        )


def convert_building(raw_data):
    extract = try_extract_value
    for e in raw_data:
        yield (
            e['buildId'],  # id
            e['builtYear'],
            e['builtQuarter'],
            e['siteId']
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

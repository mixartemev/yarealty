def userConvert(raw_data: list):
    for u in raw_data:
        yield (
            u['id'],
            u['name'],
            u['creation_date'],
            u['is_profi'],
            u['is_private_broker'],
            u['is_moderation_passed'],
            u['status'],
            u['account_type'],
            u['phones']
        )

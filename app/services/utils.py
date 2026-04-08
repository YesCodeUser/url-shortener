import shortuuid


def generate_short_id() -> str:
    return shortuuid.ShortUUID().random(length=8)

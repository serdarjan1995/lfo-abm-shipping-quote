def try_parse_int(value: str):
    value = value.strip()
    try:
        value_stripped = value.replace("$", '').strip()
        return int(value_stripped)
    except (Exception, ValueError):
        return value


def try_parse_float(value: str):
    value = value.strip()
    try:
        value_stripped = value.replace("$", '').strip()
        if value_stripped == "#N/A":
            return 0
        return float(value_stripped)
    except (Exception, ValueError):
        return value

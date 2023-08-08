def bool_validator(value):
    if value in ["true", 1, "1", True, "True"]:
        return True
    else:
        return False
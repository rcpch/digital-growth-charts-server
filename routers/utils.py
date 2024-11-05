def format_error(loc, msg, error_type, input=None):
    return {
        "loc": loc,
        "msg": msg,
        "type": error_type,
        "input": input
    }
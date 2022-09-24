from src.enums.status_code import StatusCode

def create_response(value, status_code = StatusCode.SUCCESS.value):
    try:
        data = value.__dict__
    except AttributeError:
        data = value

    return { 'data': data }, status_code

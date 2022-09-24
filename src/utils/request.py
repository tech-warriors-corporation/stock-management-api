from src.enums.status_code import StatusCode
from src.utils.error import customized_error

def create_response(value = None, status_code = StatusCode.SUCCESS.value):
    try:
        data = value.__dict__
    except:
        customized_error('value.__dict__')

        data = value

    return { 'data': data }, status_code

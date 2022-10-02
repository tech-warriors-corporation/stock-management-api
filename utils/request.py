from enums.status_code import StatusCode
from utils.error import customized_error

def create_response(value = None, status_code = StatusCode.OK.value, count = None):
    try:
        data = value.__dict__
    except:
        customized_error('value.__dict__')

        data = value

    return { 'data': data, 'count': count }, status_code

from flask import request
from utils.auth import has_valid_token, unauthorized_response
from enums.header_request import HeaderRequest

def login_required(callback):
    def secure_function(*args, **kwargs):
        token = request.headers.get(HeaderRequest.TOKEN.value)

        if has_valid_token(token):
            return callback(*args, **kwargs)
        else:
            return unauthorized_response()

    secure_function.__name__ = callback.__name__

    return secure_function

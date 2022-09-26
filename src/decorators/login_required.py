from flask import request
from src.utils.auth import has_valid_token, unauthorized_response
from src.enums.header_request import HeaderRequest

def login_required(callback):
    def secure_function():
        token = request.headers.get(HeaderRequest.TOKEN.value)

        if has_valid_token(token):
            return callback()
        else:
            return unauthorized_response()

    return secure_function

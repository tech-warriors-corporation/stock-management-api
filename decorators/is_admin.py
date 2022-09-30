from flask import request
from utils.auth import unauthorized_response
from enums.header_request import HeaderRequest
from utils.token import decoder
from enums.boolean_as_number import BooleanAsNumber

def is_admin(callback):
    def secure_function():
        token = request.headers.get(HeaderRequest.TOKEN.value)
        user = decoder(token)

        if user['is_admin'] == BooleanAsNumber.TRUE.value:
            return callback()
        else:
            return unauthorized_response()

    return secure_function

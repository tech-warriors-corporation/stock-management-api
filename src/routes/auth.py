from flask import request
from src.services.setup import app
from src.enums.http_method import HttpMethod
from src.utils.connection import get_connection
from src.utils.request import create_response
from src.enums.table import Table
from src.entities.user import User
from src.enums.status_code import StatusCode
from cryptocode import decrypt
from src.enums.crypt_type import CryptType
from src.utils.token import encoder, decoder
from src.utils.date import format_to_iso
from src.enums.header_request import HeaderRequest
from src.utils.auth import has_valid_token, unauthorized_response
from src.enums.boolean_as_number import BooleanAsNumber
from src.utils.constants import api_prefix

@app.route(f'/{api_prefix}/login', methods=[HttpMethod.POST.value])
def login():
    try:
        values = request.get_json()
        connection = get_connection()
        cursor = connection.cursor()
        email = values['email']
        user_password = values['user_password']

        cursor.execute(f"SELECT * FROM {Table.USERS.value} WHERE EMAIL='{email}' AND IS_ACTIVE={BooleanAsNumber.TRUE.value}")

        result = cursor.fetchone()
        encrypted_password = result[3]
        decrypted_password = decrypt(encrypted_password, CryptType.PASSWORD.value)

        cursor.close()

        if user_password == decrypted_password:
            token = encoder(User(result[0], result[1], result[2], encrypted_password, result[4], result[5], format_to_iso(result[6]), format_to_iso(result[7]), result[8]).__dict__)

            return create_response(token, StatusCode.SUCCESS.value)

        return create_response(None, StatusCode.FORM_ERROR.value)
    except:
        return create_response(None, StatusCode.FORM_ERROR.value)

@app.route(f'/{api_prefix}/user_by_token', methods=[HttpMethod.GET.value])
def user_by_token():
    token = request.headers.get(HeaderRequest.TOKEN.value)

    if has_valid_token(token):
        return create_response(decoder(token))
    else:
        return unauthorized_response()

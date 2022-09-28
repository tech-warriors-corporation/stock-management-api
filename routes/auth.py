from flask import request
from enums.http_method import HttpMethod
from utils.connection import get_connection
from utils.request import create_response
from enums.table import Table
from entities.user import User
from enums.status_code import StatusCode
from cryptocode import decrypt
from enums.crypt_type import CryptType
from utils.token import encoder, decoder
from utils.date import format_to_iso
from enums.header_request import HeaderRequest
from enums.boolean_as_number import BooleanAsNumber
from utils.constants import api_prefix
from decorators.login_required import login_required
from services.setup import app

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
@login_required
def user_by_token():
    token = request.headers.get(HeaderRequest.TOKEN.value)

    return create_response(decoder(token))

from utils.token import decoder
from enums.table import Table
from utils.connection import get_connection
from enums.boolean_as_number import BooleanAsNumber
from utils.request import create_response
from enums.status_code import StatusCode

def has_valid_token(token):
    try:
        user_by_token = decoder(token)
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT USER_ID FROM {Table.USERS.value} WHERE EMAIL='{user_by_token['email']}' AND USER_ID={user_by_token['user_id']} AND USER_NAME='{user_by_token['user_name']}' AND USER_PASSWORD='{user_by_token['user_password']}' AND IS_ADMIN={user_by_token['is_admin']} AND IS_ACTIVE={BooleanAsNumber.TRUE.value}")

        result = cursor.fetchone()

        cursor.close()

        return result is not None
    except:
        return False

def unauthorized_response():
    return create_response(status_code=StatusCode.UNAUTHORIZED.value)

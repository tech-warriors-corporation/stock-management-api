from src.utils.token import decoder
from src.enums.table import Table
from src.utils.connection import get_connection
from src.enums.boolean_as_number import BooleanAsNumber
from src.utils.request import create_response
from src.enums.status_code import StatusCode

def has_valid_token(token):
    try:
        user_by_token = decoder(token)
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {Table.USERS.value} WHERE EMAIL='{user_by_token['email']}' AND USER_ID={user_by_token['user_id']} AND USER_NAME='{user_by_token['user_name']}' AND USER_PASSWORD='{user_by_token['user_password']}' AND IS_ACTIVE={BooleanAsNumber.TRUE.value}")

        result = cursor.fetchone()

        cursor.close()

        return result is not None
    except:
        return False

def unauthorized_response():
    return create_response(status_code=StatusCode.UNAUTHORIZED.value)

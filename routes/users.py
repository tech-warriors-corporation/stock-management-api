from enums.http_method import HttpMethod
from utils.request import create_response
from utils.constants import api_prefix
from decorators.login_required import login_required
from decorators.is_admin import is_admin
from services.setup import app
from utils.connection import get_connection
from enums.table import Table
from enums.boolean_as_number import BooleanAsNumber
from enums.status_code import StatusCode
from flask import request
from entities.user import User

@app.route(f'/{api_prefix}/users', methods=[HttpMethod.GET.value])
@login_required
@is_admin
def users():
    try:
        query_params = request.args.to_dict()
        page = int(query_params.get('page'))
        per_page = int(query_params.get('per_page'))
        user_name = query_params.get('user_name')
        email = query_params.get('email')
        connection = get_connection()
        cursor = connection.cursor()
        where = f"WHERE IS_ACTIVE={BooleanAsNumber.TRUE.value}"
        data = []

        if user_name is not None:
            where = f"{where} AND LOWER(USER_NAME) LIKE LOWER('%{user_name}%')"

        if email is not None:
            where = f"{where} AND LOWER(EMAIL) LIKE LOWER('%{email}%')"

        cursor.execute(f"SELECT USER_ID, USER_NAME, EMAIL, IS_ADMIN, IS_ACTIVE FROM {Table.USERS.value} {where} ORDER BY USER_NAME, DT_CREATED OFFSET {page * per_page} ROWS FETCH NEXT {per_page} ROWS ONLY")

        items = cursor.fetchall()

        for item in items:
            data.append(User(item[0], item[1], item[2], None, item[3], item[4], None, None, None).__dict__)

        cursor.execute(f"SELECT COUNT(*) FROM {Table.USERS.value} {where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/users/<int:user_id>', methods=[HttpMethod.DELETE.value])
@login_required
@is_admin
def delete_user(user_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"UPDATE {Table.USERS.value} SET IS_ACTIVE = {BooleanAsNumber.FALSE.value} WHERE USER_ID = {user_id} AND IS_ACTIVE = {BooleanAsNumber.TRUE.value} AND IS_ADMIN = {BooleanAsNumber.FALSE.value}")
        connection.commit()
        cursor.close()

        return create_response(None)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

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
        page = query_params.get('page')
        per_page = 10
        connection = get_connection()
        cursor = connection.cursor()
        where = f"WHERE IS_ACTIVE={BooleanAsNumber.TRUE.value}"
        data = []

        cursor.execute(f"SELECT USER_ID, USER_NAME, EMAIL, IS_ADMIN, IS_ACTIVE FROM {Table.USERS.value} {where} ORDER BY USER_NAME OFFSET {page * per_page} ROWS FETCH NEXT {per_page} ROWS ONLY")

        items = cursor.fetchall()

        for item in items:
            data.append(User(item[0], item[1], item[2], None, item[3], item[4], None, None, None).__dict__)

        cursor.execute(f"SELECT COUNT(*) FROM {Table.USERS.value} {where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.FORM_ERROR.value)

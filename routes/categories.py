from services.setup import app
from utils.constants import api_prefix
from enums.http_method import HttpMethod
from decorators.login_required import login_required
from decorators.is_admin import is_admin
from utils.request import create_response
from enums.status_code import StatusCode
from enums.boolean_as_number import BooleanAsNumber
from enums.table import Table
from entities.category import Category
from utils.connection import get_connection
from flask import request
from utils.token import decoder
from enums.header_request import HeaderRequest

@app.route(f'/{api_prefix}/categories', methods=[HttpMethod.GET.value])
@login_required
@is_admin
def categories():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query_params = request.args.to_dict()
        page = int(query_params.get('page'))
        per_page = int(query_params.get('per_page'))
        category_name = query_params.get('category_name')
        where = f"WHERE IS_ACTIVE = {BooleanAsNumber.TRUE.value}"
        data = []

        if category_name is not None:
            where = f"{where} AND LOWER(CATEGORY_NAME) LIKE LOWER('%{category_name}%')"

        cursor.execute(f"SELECT CATEGORY_ID, CATEGORY_NAME, IS_ACTIVE FROM {Table.CATEGORIES.value} {where} ORDER BY LOWER(CATEGORY_NAME), DT_CREATED DESC, CATEGORY_ID DESC OFFSET {page * per_page} ROWS FETCH NEXT {per_page} ROWS ONLY")

        items = cursor.fetchall()

        for item in items:
            data.append(Category(item[0], item[1], None, item[2], None, None).__dict__)

        cursor.execute(f"SELECT COUNT(*) FROM {Table.CATEGORIES.value} {where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/categories/<int:category_id>', methods=[HttpMethod.DELETE.value])
@login_required
@is_admin
def delete_category(category_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"UPDATE {Table.CATEGORIES.value} SET IS_ACTIVE = {BooleanAsNumber.FALSE.value}, DT_UPDATED = SYSDATE WHERE CATEGORY_ID = {category_id} AND IS_ACTIVE = {BooleanAsNumber.TRUE.value}")
        connection.commit()
        cursor.close()

        return create_response(None)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/categories', methods=[HttpMethod.POST.value])
@login_required
@is_admin
def new_category():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        token = request.headers.get(HeaderRequest.TOKEN.value)
        user = decoder(token)
        values = request.get_json()
        category_name = values['category_name']

        cursor.execute(
            f"INSERT INTO "
            f"{Table.CATEGORIES.value}(CATEGORY_ID, CATEGORY_NAME, IS_ACTIVE, DT_CREATED, CREATED_BY_USER_ID) "
            f"VALUES(INDEX_CATEGORY.NEXTVAL, '{category_name}', {BooleanAsNumber.TRUE.value}, SYSDATE, {user['user_id']})"
        )

        connection.commit()
        cursor.close()

        return create_response(None)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/categories/<int:category_id>', methods=[HttpMethod.GET.value])
@login_required
def get_category(category_id, only_active = True):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        where = f"WHERE CATEGORY_ID = {category_id}"

        if only_active:
            where = f"{where} AND IS_ACTIVE = {BooleanAsNumber.TRUE.value}"

        cursor.execute(f"SELECT CATEGORY_NAME, IS_ACTIVE FROM {Table.CATEGORIES.value} {where}")

        result = cursor.fetchone()

        cursor.close()

        return create_response(Category(category_id, result[0], None, result[1], None, None))
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/categories/<int:category_id>', methods=[HttpMethod.PATCH.value])
@login_required
@is_admin
def edit_category(category_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        values = request.get_json()
        category_name = values['category_name']

        cursor.execute(f"UPDATE {Table.CATEGORIES.value} SET CATEGORY_NAME = '{category_name}', DT_UPDATED = SYSDATE WHERE CATEGORY_ID = {category_id} AND IS_ACTIVE = {BooleanAsNumber.TRUE.value}")

        connection.commit()
        cursor.close()

        return create_response()
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/categories/autocomplete', methods=[HttpMethod.GET.value])
@login_required
def get_autocomplete_categories():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        data = []
        query_params = request.args.to_dict()
        is_active = query_params.get('is_active')
        where = ''

        if is_active is not None and is_active.isnumeric():
            where = f"WHERE IS_ACTIVE = {int(is_active)}"

        cursor.execute(f"SELECT CATEGORY_ID, CATEGORY_NAME, IS_ACTIVE FROM {Table.CATEGORIES.value} {where} ORDER BY LOWER(CATEGORY_NAME), DT_CREATED DESC, CATEGORY_ID DESC")

        items = cursor.fetchall()

        cursor.close()

        for item in items:
            data.append(Category(item[0], item[1], None, item[2], None, None).__dict__)

        return create_response(data)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

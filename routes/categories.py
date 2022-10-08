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

        cursor.execute(f"SELECT CATEGORY_ID, CATEGORY_NAME FROM {Table.CATEGORIES.value} {where} ORDER BY LOWER(CATEGORY_NAME), DT_CREATED, CATEGORY_ID OFFSET {page * per_page} ROWS FETCH NEXT {per_page} ROWS ONLY")

        items = cursor.fetchall()

        for item in items:
            data.append(Category(item[0], item[1], None, BooleanAsNumber.TRUE.value, None, None).__dict__)

        cursor.execute(f"SELECT COUNT(*) FROM {Table.CATEGORIES.value} {where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

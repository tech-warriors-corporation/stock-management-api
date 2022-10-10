from services.setup import app
from utils.constants import api_prefix
from enums.http_method import HttpMethod
from decorators.login_required import login_required
from decorators.is_admin import is_admin
from utils.request import create_response
from enums.status_code import StatusCode
from enums.boolean_as_number import BooleanAsNumber
from enums.table import Table
from entities.product import Product
from utils.connection import get_connection
from flask import request
from routes.categories import get_category

@app.route(f'/{api_prefix}/products', methods=[HttpMethod.GET.value])
@login_required
@is_admin
def products():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query_params = request.args.to_dict()
        page = int(query_params.get('page'))
        per_page = int(query_params.get('per_page'))
        product_name = query_params.get('product_name')
        category_id = query_params.get('category_id')
        where = f"WHERE IS_ACTIVE = {BooleanAsNumber.TRUE.value}"
        data = []

        if product_name is not None:
            where = f"{where} AND LOWER(PRODUCT_NAME) LIKE LOWER('%{product_name}%')"

        if category_id is not None:
            where = f"{where} AND CATEGORY_ID = {int(category_id)}"

        cursor.execute(f"SELECT PRODUCT_ID, PRODUCT_NAME, CATEGORY_ID FROM {Table.PRODUCTS.value} {where} ORDER BY LOWER(PRODUCT_NAME), DT_CREATED, PRODUCT_ID OFFSET {page * per_page} ROWS FETCH NEXT {per_page} ROWS ONLY")

        items = cursor.fetchall()

        for item in items:
            category_id = item[2]
            category_response = get_category(category_id)[0]
            category_name = category_response['data']['category_name']

            data.append(Product(item[0], None, item[1], None, None, BooleanAsNumber.TRUE.value, None, None, category_name).__dict__)

        cursor.execute(f"SELECT COUNT(*) FROM {Table.PRODUCTS.value} {where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

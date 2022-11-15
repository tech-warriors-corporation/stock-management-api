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
from utils.token import decoder
from enums.header_request import HeaderRequest

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

        if category_id is not None and category_id.isnumeric():
            where = f"{where} AND CATEGORY_ID = {int(category_id)}"

        cursor.execute(f"SELECT PRODUCT_ID, PRODUCT_NAME, CATEGORY_ID, IS_ACTIVE, QUANTITY FROM {Table.PRODUCTS.value} {where} ORDER BY LOWER(PRODUCT_NAME), DT_CREATED DESC, PRODUCT_ID DESC OFFSET {page * per_page} ROWS FETCH NEXT {per_page} ROWS ONLY")

        items = cursor.fetchall()

        for item in items:
            category_id = item[2]
            category_data = get_category(category_id, False)[0]['data']
            category_name = category_data['category_name']
            category_is_active = category_data['is_active']

            data.append(Product(item[0], None, item[1], item[4], None, item[3], None, None, category_name, category_is_active).__dict__)

        cursor.execute(f"SELECT COUNT(*) FROM {Table.PRODUCTS.value} {where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/products/<int:product_id>', methods=[HttpMethod.DELETE.value])
@login_required
@is_admin
def delete_product(product_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"UPDATE {Table.PRODUCTS.value} SET IS_ACTIVE = {BooleanAsNumber.FALSE.value}, DT_UPDATED = SYSDATE WHERE PRODUCT_ID = {product_id} AND IS_ACTIVE = {BooleanAsNumber.TRUE.value}")
        connection.commit()
        cursor.close()

        return create_response(None)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/products', methods=[HttpMethod.POST.value])
@login_required
@is_admin
def new_product():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        token = request.headers.get(HeaderRequest.TOKEN.value)
        user = decoder(token)
        values = request.get_json()
        product_name = values['product_name']
        category_id = values['category_id']
        quantity = values['quantity']

        cursor.execute(
            f"INSERT INTO "
            f"{Table.PRODUCTS.value}(PRODUCT_ID, CATEGORY_ID, PRODUCT_NAME, QUANTITY, CREATED_BY_USER_ID, IS_ACTIVE, DT_CREATED, DT_UPDATED) "
            f"VALUES(INDEX_PRODUCT.NEXTVAL, {category_id}, '{product_name}', {quantity}, {user['user_id']}, {BooleanAsNumber.TRUE.value}, SYSDATE, NULL)"
        )

        connection.commit()
        cursor.close()

        return create_response(None)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/products/<int:product_id>', methods=[HttpMethod.GET.value])
@login_required
def get_product(product_id, only_active = True):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        where = f"WHERE PRODUCT_ID = {product_id}"

        if only_active:
            where = f"{where} AND IS_ACTIVE = {BooleanAsNumber.TRUE.value}"

        cursor.execute(f"SELECT CATEGORY_ID, PRODUCT_NAME, QUANTITY, IS_ACTIVE FROM {Table.PRODUCTS.value} {where}")

        result = cursor.fetchone()
        category_id = result[0]
        category_data = get_category(category_id, False)[0]['data']

        cursor.close()

        return create_response(Product(product_id, category_id, result[1], result[2], None, result[3], None, None, None, category_data['is_active']))
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/products/<int:product_id>', methods=[HttpMethod.PATCH.value])
@login_required
@is_admin
def edit_product(product_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        values = request.get_json()
        product_name = values['product_name']
        category_id = values['category_id']

        cursor.execute(
            f"UPDATE {Table.PRODUCTS.value} "
            f"SET PRODUCT_NAME = '{product_name}', CATEGORY_ID = {category_id}, DT_UPDATED = SYSDATE "
            f"WHERE PRODUCT_ID = {product_id} AND IS_ACTIVE = {BooleanAsNumber.TRUE.value}"
        )

        connection.commit()
        cursor.close()

        return create_response()
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/products/autocomplete', methods=[HttpMethod.GET.value])
@login_required
def get_autocomplete_products():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        data = []

        cursor.execute(f"SELECT PRODUCT_ID, PRODUCT_NAME, IS_ACTIVE FROM {Table.PRODUCTS.value} ORDER BY LOWER(PRODUCT_NAME), DT_CREATED DESC, PRODUCT_ID DESC")

        items = cursor.fetchall()

        cursor.close()

        for item in items:
            data.append(Product(item[0], None, item[1], None, None, item[2], None, None, None, None).__dict__)

        return create_response(data)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

def update_product_quantity(product_id, quantity, is_to_add, cursor):
    try:
        product = get_product(product_id, False)[0]['data']
        next_quantity = product['quantity']

        if is_to_add:
            next_quantity += quantity
        else:
            next_quantity -= quantity

        cursor.execute(
            f"UPDATE {Table.PRODUCTS.value} "
            f"SET QUANTITY = {next_quantity}, DT_UPDATED = SYSDATE "
            f"WHERE PRODUCT_ID = {product_id}"
        )

        return create_response()
    except:
        message = None

        if not is_to_add:
            message = 'Quantidade do produto não pode ser negativa'

        return create_response(message, StatusCode.BAD_REQUEST.value)

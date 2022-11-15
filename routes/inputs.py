from services.setup import app
from utils.constants import api_prefix
from enums.http_method import HttpMethod
from decorators.login_required import login_required
from utils.request import create_response
from enums.status_code import StatusCode
from enums.boolean_as_number import BooleanAsNumber
from enums.table import Table
from entities.input import Input
from utils.connection import get_connection
from flask import request
from utils.date import format_to_iso, date_text_format
from routes.products import get_product, update_product_quantity
from routes.categories import get_category
from routes.users import get_user

@app.route(f'/{api_prefix}/inputs', methods=[HttpMethod.GET.value])
@login_required
def inputs():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query_params = request.args.to_dict()
        page = int(query_params.get('page'))
        per_page = int(query_params.get('per_page'))
        product_id = query_params.get('product_id')
        has_product_expiration = query_params.get('has_product_expiration')
        created_by_id = query_params.get('created_by_id')
        dt_created = query_params.get('dt_created')
        from_and_where = f"FROM {Table.INPUTS.value} WHERE INPUT_ID IS NOT NULL"
        data = []

        if product_id is not None and product_id.isnumeric():
            from_and_where = f"{from_and_where} AND PRODUCT_ID = {int(product_id)}"

        if has_product_expiration is not None and has_product_expiration.isnumeric():
            from_and_where = f"{from_and_where} AND HAS_PRODUCT_EXPIRATION = {int(has_product_expiration)}"

        if created_by_id is not None and created_by_id.isnumeric():
            from_and_where = f"{from_and_where} AND CREATED_BY_USER_ID = {int(created_by_id)}"

        if dt_created is not None:
            from_and_where = f"{from_and_where} AND TRUNC(DT_CREATED) = TO_DATE('{dt_created}', '{date_text_format}')"

        cursor.execute(
            f"SELECT INPUT_ID, PRODUCT_ID, PRODUCT_QUANTITY, HAS_PRODUCT_EXPIRATION, IS_DONATION, CREATED_BY_USER_ID, DT_ENTERED, DT_CREATED, UNIT_PRICE, INPUT_DESCRIPTION "
            f"{from_and_where} ORDER BY DT_ENTERED DESC, DT_CREATED DESC, INPUT_ID DESC OFFSET {page * per_page} ROWS FETCH NEXT {per_page} ROWS ONLY"
        )

        items = cursor.fetchall()

        for item in items:
            input_id = item[0]
            product_id = item[1]
            product = get_product(product_id, False)[0]['data']
            category_id = product['category_id']
            category = get_category(category_id, False)[0]['data']
            product_quantity = item[2]
            has_product_expiration = item[3]
            is_donation = item[4]
            created_by_user_id = item[5]
            created_by = get_user(created_by_user_id, False)[0]['data']
            dt_entered = format_to_iso(item[6])
            dt_created = format_to_iso(item[7])
            unit_price = item[8]
            input_description = item[9]

            data.append(Input(input_id, product, category, product_quantity, has_product_expiration, is_donation, created_by, dt_entered, dt_created, None, unit_price, input_description).__dict__)

        cursor.execute(f"SELECT COUNT(*) {from_and_where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/inputs/<int:input_id>', methods=[HttpMethod.GET.value])
@login_required
def get_input(input_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        from_and_where = f"FROM {Table.INPUTS.value} WHERE INPUT_ID = {input_id}"

        cursor.execute(f"SELECT INPUT_ID, PRODUCT_ID, PRODUCT_QUANTITY {from_and_where}")

        result = cursor.fetchone()
        product_id = result[1]
        product = get_product(product_id, False)[0]['data']

        cursor.close()

        return create_response(Input(input_id, product, None, result[2], None, None, None, None, None, None, None, None))
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/inputs/<int:input_id>', methods=[HttpMethod.DELETE.value])
@login_required
def delete_input(input_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        input_data = get_input(input_id)[0]['data']
        product = input_data['product']
        response = update_product_quantity(product['product_id'], input_data['product_quantity'], False, cursor)
        result = response[0]
        status_code = response[1]

        if status_code == StatusCode.BAD_REQUEST.value:
            return create_response(result['data'], StatusCode.BAD_REQUEST.value)

        cursor.execute(f"DELETE FROM {Table.INPUTS.value} WHERE INPUT_ID = {input_id}")
        connection.commit()
        cursor.close()

        return create_response()
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

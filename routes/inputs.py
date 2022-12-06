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
from utils.date import format_to_iso, date_text_format, date_save_format, format_to_save_date, get_year
from routes.products import get_product, update_product_quantity
from routes.categories import get_category
from routes.users import get_user
from utils.token import decoder
from enums.header_request import HeaderRequest
from utils.string import string_to_varchar

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

        cursor.execute(f"SELECT PRODUCT_ID, PRODUCT_QUANTITY, HAS_PRODUCT_EXPIRATION, IS_DONATION, DT_ENTERED, DT_CREATED, UNIT_PRICE, INPUT_DESCRIPTION {from_and_where}")

        result = cursor.fetchone()
        product_id = result[0]
        product = get_product(product_id, False)[0]['data']

        cursor.close()

        return create_response(Input(input_id, product, None, result[1], result[2], result[3], None, format_to_iso(result[4]), format_to_iso(result[5]), None, result[6], result[7]))
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

@app.route(f'/{api_prefix}/inputs', methods=[HttpMethod.POST.value])
@login_required
def new_input():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        token = request.headers.get(HeaderRequest.TOKEN.value)
        user = decoder(token)
        values = request.get_json()
        product_id = values['product_id']
        product_quantity = values['product_quantity']
        has_product_expiration = values['has_product_expiration']
        is_donation = values['is_donation']
        dt_entered = f"TO_DATE('{format_to_save_date(values['dt_entered'])}', '{date_save_format}')"
        unit_price = values['unit_price']
        input_description = values['input_description']
        input_description_sql_format = string_to_varchar(input_description)
        response = update_product_quantity(product_id, product_quantity, True, cursor)
        result = response[0]
        status_code = response[1]

        if status_code == StatusCode.BAD_REQUEST.value:
            return create_response(result['data'], StatusCode.BAD_REQUEST.value)

        cursor.execute(
            f"INSERT INTO "
            f"{Table.INPUTS.value}(INPUT_ID, PRODUCT_ID, PRODUCT_QUANTITY, HAS_PRODUCT_EXPIRATION, IS_DONATION, CREATED_BY_USER_ID, DT_ENTERED, DT_CREATED, DT_UPDATED, UNIT_PRICE, INPUT_DESCRIPTION) "
            f"VALUES(INDEX_INPUT.NEXTVAL, {product_id}, {product_quantity}, {has_product_expiration}, {is_donation}, {user['user_id']}, {dt_entered}, SYSDATE, NULL, {unit_price if unit_price is not None else 'NULL'}, {input_description_sql_format if input_description is not None else 'NULL'})"
        )

        connection.commit()
        cursor.close()

        return create_response(None)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/inputs/<int:input_id>', methods=[HttpMethod.PATCH.value])
@login_required
def edit_input(input_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        values = request.get_json()
        has_product_expiration = values['has_product_expiration']
        is_donation = values['is_donation']
        unit_price = values['unit_price']
        input_description = values['input_description']
        input_description_sql_format = string_to_varchar(input_description)

        cursor.execute(
            f"UPDATE {Table.INPUTS.value} "
            f"SET HAS_PRODUCT_EXPIRATION = {has_product_expiration}, IS_DONATION = {is_donation}, UNIT_PRICE = {unit_price if unit_price is not None else 'NULL'}, INPUT_DESCRIPTION = {input_description_sql_format if input_description is not None else 'NULL'}, DT_UPDATED = SYSDATE "
            f"WHERE INPUT_ID = {input_id}"
        )

        connection.commit()
        cursor.close()

        return create_response()
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/inputs/products_donated', methods=[HttpMethod.GET.value])
@login_required
def get_products_donated():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query_params = request.args.to_dict()
        year = get_year(query_params.get('year'))

        cursor.execute(
            f"SELECT COUNT(*) "
            f"FROM {Table.INPUTS.value} "
            f"WHERE IS_DONATION = {BooleanAsNumber.TRUE.value} AND TRUNC(DT_ENTERED) BETWEEN TO_DATE('01-01-{year}', '{date_text_format}') AND TO_DATE('31-12-{year}', '{date_text_format}')"
        )

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(None, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/inputs/invested_money', methods=[HttpMethod.GET.value])
@login_required
def get_invested_money():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query_params = request.args.to_dict()
        year = get_year(query_params.get('year'))
        value = 0

        cursor.execute(
            f"SELECT PRODUCT_QUANTITY, UNIT_PRICE "
            f"FROM {Table.INPUTS.value} "
            f"WHERE IS_DONATION = {BooleanAsNumber.FALSE.value} AND TRUNC(DT_ENTERED) BETWEEN TO_DATE('01-01-{year}', '{date_text_format}') AND TO_DATE('31-12-{year}', '{date_text_format}')"
        )

        items = cursor.fetchall()

        for item in items:
            value += item[0] * item[1]

        cursor.close()

        return create_response(value)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

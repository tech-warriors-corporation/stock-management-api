from services.setup import app
from utils.constants import api_prefix
from enums.http_method import HttpMethod
from utils.connection import get_connection
from flask import request
from utils.request import create_response
from enums.status_code import StatusCode
from enums.table import Table
from utils.date import date_text_format, format_to_iso, date_save_format, format_to_save_date, get_year
from decorators.login_required import login_required
from entities.output import Output
from routes.products import get_product, update_product_quantity
from routes.categories import get_category
from routes.users import get_user
from enums.header_request import HeaderRequest
from utils.token import decoder
from utils.string import string_to_varchar

@app.route(f'/{api_prefix}/outputs', methods=[HttpMethod.GET.value])
@login_required
def outputs():
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
        from_and_where = f"FROM {Table.OUTPUTS.value} WHERE OUTPUT_ID IS NOT NULL"
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
            f"SELECT OUTPUT_ID, PRODUCT_ID, PRODUCT_QUANTITY, HAS_PRODUCT_EXPIRATION, PRODUCT_WENT_TO, CREATED_BY_USER_ID, DT_EXITED, DT_CREATED, OUTPUT_DESCRIPTION "
            f"{from_and_where} ORDER BY DT_EXITED DESC, DT_CREATED DESC, OUTPUT_ID DESC OFFSET {page * per_page} ROWS FETCH NEXT {per_page} ROWS ONLY"
        )

        items = cursor.fetchall()

        for item in items:
            output_id = item[0]
            product_id = item[1]
            product = get_product(product_id, False)[0]['data']
            category_id = product['category_id']
            category = get_category(category_id, False)[0]['data']
            product_quantity = item[2]
            has_product_expiration = item[3]
            product_went_to = item[4]
            created_by_user_id = item[5]
            created_by = get_user(created_by_user_id, False)[0]['data']
            dt_exited = format_to_iso(item[6])
            dt_created = format_to_iso(item[7])
            output_description = item[8]

            data.append(Output(output_id, product, category, product_quantity, has_product_expiration, product_went_to, created_by, dt_exited, dt_created, None, output_description).__dict__)

        cursor.execute(f"SELECT COUNT(*) {from_and_where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/outputs/<int:output_id>', methods=[HttpMethod.GET.value])
@login_required
def get_output(output_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        from_and_where = f"FROM {Table.OUTPUTS.value} WHERE OUTPUT_ID = {output_id}"

        cursor.execute(f"SELECT PRODUCT_ID, PRODUCT_QUANTITY, HAS_PRODUCT_EXPIRATION, PRODUCT_WENT_TO, DT_EXITED, DT_CREATED, OUTPUT_DESCRIPTION {from_and_where}")

        result = cursor.fetchone()
        product_id = result[0]
        product = get_product(product_id, False)[0]['data']
        product_quantity = result[1]
        has_product_expiration = result[2]
        product_went_to = result[3]
        dt_exited = format_to_iso(result[4])
        dt_created = format_to_iso(result[5])
        output_description = result[6]

        cursor.close()

        return create_response(Output(output_id, product, None, product_quantity, has_product_expiration, product_went_to, None, dt_exited, dt_created, None, output_description))
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/outputs/<int:output_id>', methods=[HttpMethod.DELETE.value])
@login_required
def delete_output(output_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        output_data = get_output(output_id)[0]['data']
        product = output_data['product']
        response = update_product_quantity(product['product_id'], output_data['product_quantity'], True, cursor)
        result = response[0]
        status_code = response[1]

        if status_code == StatusCode.BAD_REQUEST.value:
            return create_response(result['data'], StatusCode.BAD_REQUEST.value)

        cursor.execute(f"DELETE FROM {Table.OUTPUTS.value} WHERE OUTPUT_ID = {output_id}")
        connection.commit()
        cursor.close()

        return create_response()
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/outputs', methods=[HttpMethod.POST.value])
@login_required
def new_output():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        token = request.headers.get(HeaderRequest.TOKEN.value)
        user = decoder(token)
        values = request.get_json()
        product_id = values['product_id']
        product_quantity = values['product_quantity']
        has_product_expiration = values['has_product_expiration']
        dt_exited = f"TO_DATE('{format_to_save_date(values['dt_exited'])}', '{date_save_format}')"
        product_went_to = values['product_went_to']
        output_description = values['output_description']
        output_description_sql_format = string_to_varchar(output_description)
        response = update_product_quantity(product_id, product_quantity, False, cursor)
        result = response[0]
        status_code = response[1]

        if status_code == StatusCode.BAD_REQUEST.value:
            return create_response(result['data'], StatusCode.BAD_REQUEST.value)

        cursor.execute(
            f"INSERT INTO "
            f"{Table.OUTPUTS.value}(OUTPUT_ID, PRODUCT_ID, PRODUCT_QUANTITY, HAS_PRODUCT_EXPIRATION, PRODUCT_WENT_TO, CREATED_BY_USER_ID, DT_EXITED, DT_CREATED, OUTPUT_DESCRIPTION) "
            f"VALUES(INDEX_OUTPUT.NEXTVAL, {product_id}, {product_quantity}, {has_product_expiration}, '{product_went_to}', {user['user_id']}, {dt_exited}, SYSDATE, {output_description_sql_format if output_description is not None else 'NULL'})"
        )

        connection.commit()
        cursor.close()

        return create_response(None)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/outputs/<int:output_id>', methods=[HttpMethod.PATCH.value])
@login_required
def edit_output(output_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        values = request.get_json()
        has_product_expiration = values['has_product_expiration']
        product_went_to = values['product_went_to']
        output_description = values['output_description']
        output_description_sql_format = string_to_varchar(output_description)

        cursor.execute(
            f"UPDATE {Table.OUTPUTS.value} "
            f"SET HAS_PRODUCT_EXPIRATION = {has_product_expiration}, PRODUCT_WENT_TO = '{product_went_to}', OUTPUT_DESCRIPTION = {output_description_sql_format if output_description is not None else 'NULL'}, DT_UPDATED = SYSDATE "
            f"WHERE OUTPUT_ID = {output_id}"
        )

        connection.commit()
        cursor.close()

        return create_response()
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

@app.route(f'/{api_prefix}/outputs/quantity', methods=[HttpMethod.GET.value])
@login_required
def get_outputs_quantity():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query_params = request.args.to_dict()
        year = get_year(query_params.get('year'))
        product_id = query_params.get('product_id')
        from_and_where = f"FROM {Table.OUTPUTS.value} WHERE TRUNC(DT_EXITED) BETWEEN TO_DATE('01-01-{year}', '{date_text_format}') AND TO_DATE('31-12-{year}', '{date_text_format}')"
        data = []

        if product_id is not None and product_id.isnumeric():
            from_and_where = f"{from_and_where} AND PRODUCT_ID = {int(product_id)}"

        cursor.execute(f"SELECT DT_EXITED {from_and_where}")

        items = cursor.fetchall()

        for item in items:
            dt_exited = format_to_iso(item[0])

            data.append(Output(None, None, None, None, None, None, None, dt_exited, None, None, None).__dict__)

        cursor.close()

        return create_response(data)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

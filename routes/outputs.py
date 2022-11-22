from services.setup import app
from utils.constants import api_prefix
from enums.http_method import HttpMethod
from utils.connection import get_connection
from flask import request
from utils.request import create_response
from enums.status_code import StatusCode
from enums.table import Table
from utils.date import date_text_format, format_to_iso
from decorators.login_required import login_required
from entities.output import Output
from routes.products import get_product
from routes.categories import get_category
from routes.users import get_user

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

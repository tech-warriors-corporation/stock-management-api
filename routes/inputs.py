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
from utils.date import format_to_iso
from routes.products import get_product
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
        from_and_where = f"FROM {Table.INPUTS.value} WHERE IS_ACTIVE = {BooleanAsNumber.TRUE.value}"
        data = []

        cursor.execute(
            f"SELECT INPUT_ID, PRODUCT_ID, PRODUCT_QUANTITY, HAS_PRODUCT_EXPIRATION, IS_DONATION, CREATED_BY_USER_ID, IS_ACTIVE, DT_ENTERED, DT_CREATED, UNIT_PRICE, INPUT_DESCRIPTION "
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
            is_active = item[6]
            dt_entered = format_to_iso(item[7])
            dt_created = format_to_iso(item[8])
            unit_price = item[9]
            input_description = item[10]

            data.append(Input(input_id, product, category, product_quantity, has_product_expiration, is_donation, created_by, is_active, dt_entered, dt_created, None, unit_price, input_description).__dict__)

        cursor.execute(f"SELECT COUNT(*) {from_and_where}")

        count = cursor.fetchone()[0]

        cursor.close()

        return create_response(data, count=count)
    except:
        return create_response(None, StatusCode.BAD_REQUEST.value)

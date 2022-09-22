from src.enums.boolean_as_number import BooleanAsNumber

class Output:
    def __init__(self, product_id, product_quantity, product_went_to, created_by_user_id, dt_exited, dt_created, output_description, has_product_expiration = BooleanAsNumber.FALSE.value, output_id = None, is_active = BooleanAsNumber.TRUE.value, dt_updated = None):
        self._output_id = output_id
        self._product_id = product_id
        self._product_quantity = product_quantity
        self._has_product_expiration = has_product_expiration
        self._product_went_to = product_went_to
        self._created_by_user_id = created_by_user_id
        self._is_active = is_active
        self._dt_exited = dt_exited
        self._dt_created = dt_created
        self._dt_updated = dt_updated
        self._output_description = output_description

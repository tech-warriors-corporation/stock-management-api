from src.enums.boolean_as_number import BooleanAsNumber

class Output:
    def __init__(self, output_id, product_id, product_quantity, has_product_expiration, product_went_to, created_by_user_id, is_active, dt_exited, dt_created, dt_updated, output_description):
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

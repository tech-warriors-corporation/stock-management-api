class Input:
    def __init__(self, input_id, product_id, product_quantity, has_product_expiration, is_donation, created_by_user_id, is_active, dt_entered, dt_created, dt_updated, unit_price, input_description):
        self._input_id = input_id
        self._product_id = product_id
        self._product_quantity = product_quantity
        self._has_product_expiration = has_product_expiration
        self._is_donation = is_donation
        self._created_by_user_id = created_by_user_id
        self._is_active = is_active
        self._dt_entered = dt_entered
        self._dt_created = dt_created
        self._dt_updated = dt_updated
        self._unit_price = unit_price
        self._input_description = input_description

from src.enums.boolean_as_number import BooleanAsNumber

class Product:
    def __init__(self, category_id, product_name, dt_created, quantity = 0, created_by_user_id = None, product_id = None, is_active = BooleanAsNumber.TRUE.value, dt_updated = None):
        self._product_id = product_id
        self._category_id = category_id
        self._product_name = product_name
        self._quantity = quantity
        self._created_by_user_id = created_by_user_id
        self._is_active = is_active
        self._dt_created = dt_created
        self._dt_updated = dt_updated

from src.enums.boolean_as_number import BooleanAsNumber

class Product:
    def __init__(self, product_id, category_id, product_name, quantity, created_by_user_id, is_active, dt_created, dt_updated):
        self._product_id = product_id
        self._category_id = category_id
        self._product_name = product_name
        self._quantity = quantity
        self._created_by_user_id = created_by_user_id
        self._is_active = is_active
        self._dt_created = dt_created
        self._dt_updated = dt_updated

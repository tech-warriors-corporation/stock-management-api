from src.enums.boolean_as_number import BooleanAsNumber

class Category:
    def __init__(self, category_name, created_by_user_id, dt_created, category_id = None, is_active = BooleanAsNumber.TRUE.value, dt_updated = None):
        self._category_id = category_id
        self._category_name = category_name
        self._created_by_user_id = created_by_user_id
        self._is_active = is_active
        self._dt_created = dt_created
        self._dt_updated = dt_updated

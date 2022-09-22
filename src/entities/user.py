from src.enums.boolean_as_number import BooleanAsNumber

class User:
    def __init__(self, user_name, email, user_password, dt_created, created_by_user_id, is_admin = BooleanAsNumber.FALSE.value, user_id = None, is_active = BooleanAsNumber.TRUE.value, dt_updated = None):
        self._user_id = user_id
        self._user_name = user_name
        self._email = email
        self._user_password = user_password
        self._is_admin = is_admin
        self._is_active = is_active
        self._dt_created = dt_created
        self._dt_updated = dt_updated
        self._created_by_user_id = created_by_user_id

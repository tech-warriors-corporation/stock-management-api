class User:
    def __init__(self, user_id, user_name, email, user_password, is_admin, is_active, dt_created, dt_updated, created_by_user_id, already_changed_password):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.user_password = user_password
        self.is_admin = is_admin
        self.is_active = is_active
        self.dt_created = dt_created
        self.dt_updated = dt_updated
        self.created_by_user_id = created_by_user_id
        self.already_changed_password = already_changed_password

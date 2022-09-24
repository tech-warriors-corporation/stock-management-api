class Category:
    def __init__(self, category_id, category_name, created_by_user_id, is_active, dt_created, dt_updated):
        self.category_id = category_id
        self.category_name = category_name
        self.created_by_user_id = created_by_user_id
        self.is_active = is_active
        self.dt_created = dt_created
        self.dt_updated = dt_updated

class Product:
    def __init__(self, product_id, category_id, product_name, quantity, created_by_user_id, is_active, dt_created, dt_updated, category_name, category_is_active):
        self.product_id = product_id
        self.category_id = category_id
        self.product_name = product_name
        self.quantity = quantity
        self.created_by_user_id = created_by_user_id
        self.is_active = is_active
        self.dt_created = dt_created
        self.dt_updated = dt_updated
        self.category_name = category_name
        self.category_is_active = category_is_active

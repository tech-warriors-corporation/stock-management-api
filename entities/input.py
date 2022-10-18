class Input:
    def __init__(self, input_id, product, category, product_quantity, has_product_expiration, is_donation, created_by, is_active, dt_entered, dt_created, dt_updated, unit_price, input_description):
        self.input_id = input_id
        self.product = product
        self.category = category
        self.product_quantity = product_quantity
        self.has_product_expiration = has_product_expiration
        self.is_donation = is_donation
        self.created_by = created_by
        self.is_active = is_active
        self.dt_entered = dt_entered
        self.dt_created = dt_created
        self.dt_updated = dt_updated
        self.unit_price = unit_price
        self.input_description = input_description

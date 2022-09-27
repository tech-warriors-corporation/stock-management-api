class Output:
    def __init__(self, output_id, product_id, product_quantity, has_product_expiration, product_went_to, created_by_user_id, is_active, dt_exited, dt_created, dt_updated, output_description):
        self.output_id = output_id
        self.product_id = product_id
        self.product_quantity = product_quantity
        self.has_product_expiration = has_product_expiration
        self.product_went_to = product_went_to
        self.created_by_user_id = created_by_user_id
        self.is_active = is_active
        self.dt_exited = dt_exited
        self.dt_created = dt_created
        self.dt_updated = dt_updated
        self.output_description = output_description

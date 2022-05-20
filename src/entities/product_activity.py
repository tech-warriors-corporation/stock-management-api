from datetime import datetime

class ProductActivity:
    def __init__(self, description, quantity, product, created_by, activity_type, has_product_expiration = None, created_at = None):
        if created_at is None:
            created_at = datetime.now()

        if has_product_expiration is None:
            has_product_expiration = False

        self._description = description
        self._quantity = quantity
        self._product = product
        self._created_by = created_by
        self._activity_type = activity_type
        self._has_product_expiration = has_product_expiration
        self._created_at = created_at

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, product):
        self._product = product

    @property
    def created_by(self):
        return self._created_by

    @property
    def activity_type(self):
        return self._activity_type.value

    @property
    def has_product_expiration(self):
        return self._has_product_expiration

    @has_product_expiration.setter
    def has_product_expiration(self, has_product_expiration):
        self._has_product_expiration = has_product_expiration

    @property
    def created_at(self):
        return self._created_at

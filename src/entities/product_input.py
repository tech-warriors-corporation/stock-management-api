from src.enums.activity_type import ActivityType

class ProductInput:
    def __init__(self, description, quantity, unit_price, product, created_by, created_at, has_product_expiration = False, is_donation = False, entered_at = None):
        self._description = description
        self._quantity = quantity
        self._unit_price = unit_price
        self._product = product
        self._created_by = created_by
        self._created_at = created_at
        self._has_product_expiration = has_product_expiration
        self._is_donation = is_donation
        self._activity_type = ActivityType.PRODUCT_INPUT

        if entered_at is None:
            self._entered_at = self._created_at
        else:
            self._entered_at = entered_at

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
    def unit_price(self):
        return self._unit_price

    @unit_price.setter
    def unit_price(self, unit_price):
        self._unit_price = unit_price

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, product):
        self._product = product

    @property
    def created_by(self):
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        self._created_by = created_by

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    @property
    def has_product_expiration(self):
        return self._has_product_expiration

    @has_product_expiration.setter
    def has_product_expiration(self, has_product_expiration):
        self._has_product_expiration = has_product_expiration

    @property
    def is_donation(self):
        return self._is_donation

    @is_donation.setter
    def is_donation(self, is_donation):
        self._is_donation = is_donation

    @property
    def entered_at(self):
        return self._entered_at

    @entered_at.setter
    def entered_at(self, entered_at):
        self._entered_at = entered_at

    @property
    def total_price(self):
        return self.unit_price * self.quantity

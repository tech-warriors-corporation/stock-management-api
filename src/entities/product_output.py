from src.enums.activity_type import ActivityType
from datetime import datetime

class ProductOutput:
    def __init__(self, description, product_went_to, quantity, product, created_by, created_at = datetime.now(), has_product_expiration = False, exited_at = None):
        self._description = description
        self._product_went_to = product_went_to
        self._quantity = quantity
        self._product = product
        self._created_by = created_by
        self._created_at = created_at
        self._has_product_expiration = has_product_expiration
        self._activity_type = ActivityType.PRODUCT_OUTPUT

        if exited_at is None:
            self._exited_at = self._created_at
        else:
            self._exited_at = exited_at

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def product_went_to(self):
        return self._product_went_to

    @product_went_to.setter
    def product_went_to(self, product_went_to):
        self._product_went_to = product_went_to

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
    def created_at(self):
        return self._created_at

    @property
    def has_product_expiration(self):
        return self._has_product_expiration

    @has_product_expiration.setter
    def has_product_expiration(self, has_product_expiration):
        self._has_product_expiration = has_product_expiration

    @property
    def activity_type(self):
        return self._activity_type.value

    @property
    def exited_at(self):
        return self._exited_at

    @exited_at.setter
    def exited_at(self, exited_at):
        self._exited_at = exited_at

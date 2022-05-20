from src.enums.activity_type import ActivityType
from product_activity import ProductActivity

class ProductInput(ProductActivity):
    def __init__(self, description, quantity, product, created_by, has_product_expiration, created_at, unit_price, is_donation = False, entered_at = None):
        super().__init__(description, quantity, product, created_by, ActivityType.PRODUCT_INPUT, has_product_expiration, created_at)

        self._unit_price = unit_price
        self._is_donation = is_donation

        if entered_at is None:
            self._entered_at = self.created_at
        else:
            self._entered_at = entered_at

    @property
    def unit_price(self):
        return self._unit_price

    @unit_price.setter
    def unit_price(self, unit_price):
        self._unit_price = unit_price

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

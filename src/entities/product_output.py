from src.enums.activity_type import ActivityType
from product_activity import ProductActivity

class ProductOutput(ProductActivity):
    def __init__(self, description, quantity, product, created_by, has_product_expiration, created_at, product_went_to, exited_at = None):
        super().__init__(description, quantity, product, created_by, ActivityType.PRODUCT_OUTPUT, has_product_expiration, created_at)

        self._product_went_to = product_went_to

        if exited_at is None:
            self._exited_at = self.created_at
        else:
            self._exited_at = exited_at

    @property
    def product_went_to(self):
        return self._product_went_to

    @product_went_to.setter
    def product_went_to(self, product_went_to):
        self._product_went_to = product_went_to

    @property
    def exited_at(self):
        return self._exited_at

    @exited_at.setter
    def exited_at(self, exited_at):
        self._exited_at = exited_at

from src.enums.boolean_as_number import BooleanAsNumber
from src.entities.user import User
from src.entities.category import Category
from src.entities.product import Product
from datetime import datetime

registered_id = 1
date = datetime.now()
user = User(registered_id, 'admin', 'email', 'password', BooleanAsNumber.TRUE.value, BooleanAsNumber.TRUE.value, date, None, None)
category = Category(registered_id, 'school', registered_id, BooleanAsNumber.TRUE.value, date, None)
product = Product(registered_id, registered_id, 'apple', 5, registered_id, BooleanAsNumber.TRUE.value, date, None)

print(user)
print(category)
print(product)

from src.enums.boolean_as_number import BooleanAsNumber
from src.entities.user import User
from src.entities.category import Category
from src.entities.product import Product
from src.entities.output import Output
from src.entities.input import Input
from datetime import datetime

registered_id = 1
date = datetime.now()
user = User(registered_id, 'admin', 'email', 'password', BooleanAsNumber.TRUE.value, BooleanAsNumber.TRUE.value, date, None, None)
category = Category(registered_id, 'school', registered_id, BooleanAsNumber.TRUE.value, date, None)
product = Product(registered_id, registered_id, 'apple', 5, registered_id, BooleanAsNumber.TRUE.value, date, None)
output = Output(registered_id, registered_id, 3, BooleanAsNumber.FALSE.value, 'person name', registered_id, BooleanAsNumber.TRUE.value, date, date, None, 'product output')
product_input = Input(registered_id, registered_id, 4, BooleanAsNumber.FALSE.value, BooleanAsNumber.FALSE.value, registered_id, BooleanAsNumber.TRUE.value, date, date, None, 400, 'product input')

print(user)
print(category)
print(product)
print(output)
print(product_input)

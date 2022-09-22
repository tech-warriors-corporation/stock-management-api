from src.enums.boolean_as_number import BooleanAsNumber
from src.entities.user import User
from datetime import datetime

user = User(None, 'admin', 'email@email.email', 'password', BooleanAsNumber.TRUE.value, BooleanAsNumber.TRUE.value, datetime.now(), None, None)

print(user)

from os import environ
from src.enums.env_var import EnvVar
from jwt import encode, decode

_secret = environ.get(EnvVar.JWT_SECRET.value)
_algorithm = environ.get(EnvVar.JWT_ALGORITHM.value)
_charset = environ.get(EnvVar.JWT_CHARSET.value)

def encoder(data):
    return encode(data, _secret, algorithm=_algorithm).decode(_charset)

def decoder(token):
    return decode(token, _secret, False, [_algorithm])

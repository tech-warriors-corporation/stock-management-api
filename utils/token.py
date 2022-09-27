from os import environ
from enums.env_var import EnvVar
from jwt import encode, decode

_secret = environ.get(EnvVar.JWT_SECRET.value)
_algorithm = environ.get(EnvVar.JWT_ALGORITHM.value)

def encoder(data):
    return encode(data, _secret, algorithm=_algorithm)

def decoder(token):
    return decode(token, _secret, [_algorithm])

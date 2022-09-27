import oracledb
from os import environ
from enums.env_var import EnvVar

_connection = None

def get_connection():
    global _connection

    if _connection is not None:
        return _connection

    _connection = oracledb.connect(
        user=environ.get(EnvVar.DB_USER.value),
        password=environ.get(EnvVar.DB_PASSWORD.value),
        host=environ.get(EnvVar.DB_HOST.value),
        port=environ.get(EnvVar.DB_PORT.value),
        sid=environ.get(EnvVar.DB_SID.value)
    )

    return get_connection()

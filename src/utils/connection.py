import oracledb
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

_connection = None

def get_connection():
    global _connection

    if _connection is not None:
        return _connection

    _connection = oracledb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), host=os.environ.get('DB_HOST'), port=os.environ.get('DB_PORT'), sid=os.environ.get('DB_SID'))

    return get_connection()

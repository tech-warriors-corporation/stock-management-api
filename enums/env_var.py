from enum import Enum

class EnvVar(Enum):
    DB_USER = 'DB_USER'
    DB_PASSWORD = 'DB_PASSWORD'
    DB_HOST = 'DB_HOST'
    DB_PORT = 'DB_PORT'
    DB_SID = 'DB_SID'
    DEBUG_MODE = 'DEBUG_MODE'
    JWT_SECRET = 'JWT_SECRET'
    JWT_ALGORITHM = 'JWT_ALGORITHM'
    ORIGIN = 'ORIGIN'
    PORT = 'PORT'

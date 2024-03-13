from mysql.connector import connection

from src.cabinet.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class Connection(metaclass=Singleton):
    def __init__(self):
        self.con = connection.MySQLConnection(
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME,
        )

    def get_connection(self) -> connection.MySQLConnection:
        return self.con

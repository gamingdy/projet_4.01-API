from src.auth.model.user import User
from src.auth.utils.funct import check_password, hash_password
from .connection import Connection


class DaoLogin:
    def __init__(self):
        self.db = Connection().get_connection()

    def login(self, username, password):
        cursor = self.db.cursor()
        hashed = hash_password(password)
        cursor.execute(
            "SELECT * FROM users WHERE login=%s",
            (username,),
        )
        user = cursor.fetchone()
        if user:
            if check_password(password, user[1]):
                cursor.close()
                user_data = User(username=user[0], role=user[3])
                return user_data

        cursor.close()
        return None

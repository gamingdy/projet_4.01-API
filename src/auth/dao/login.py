from src.auth.model.user import ConnectedUser
from src.auth.utils.funct import check_password, hash_password
from .connection import Connection


class DaoLogin:
    def __init__(self):
        self.db = Connection().get_connection()

    def login(self, username, password) -> ConnectedUser | None:
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
                user_data = ConnectedUser(username=user[0])
                return user_data

        cursor.close()
        return None

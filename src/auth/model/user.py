from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class ConnectedUser:
    def __init__(self, username):
        self.username = username

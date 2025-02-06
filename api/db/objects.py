"""Holds classes of all objects for database use"""

class User():
    def __init__(self, username: str, password: str, userId: int = -1):
        self.UserId = userId
        self.Username = username
        self.Password = password

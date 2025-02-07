"""Used to hold the information about the database and commands used with it"""

import sqlite3
from objects import User

class Database_Connection():
    """Used as a singleton to access the database"""
    
    def __new__(self):
        """Handles ensuring that this class is a singleton"""
        if not hasattr(self, 'instance'):
            self.instance = super(Database_Connection, self).__new__(self)
        return self.instance
    
    def __init__(self):
        """Handles initializing the class"""
        self.conn = sqlite3.connect('cookbook.db')
        self.cursor = self.conn.cursor()

        # Checking if the tables exist
        userTable = self.cursor.execute("SELECT tableName FROM sqlite_master WHERE type='table' AND tableName='Users'").fetchone()
        if userTable is None:
            with open("my_script.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

    def add_user(self, user: User) -> bool:
        """Adds a new user to the database"""
        try:
            commandString: str = "INSERT INTO Users (Username, Password) VALUES (%s, %s)"
            self.cursor.execute(commandString, user.Username, user.Password)
            self.conn.commit()
            return True
        except:
            return False
        
    def get_user(self, username: str) -> User:
        """Gets a user based on their username"""
        commandString: str = "SELECT * FROM Users WHERE USERNAME = %s"
        self.cursor.execute(commandString, username)
        user: User = self.cursor.fetchone()
        return user
    
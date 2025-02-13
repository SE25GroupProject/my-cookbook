"""Used to hold the information about the database and commands used with it"""

import sqlite3
from db.objects import User

class Database_Connection():
    """Used as a singleton to access the database"""

    def convert_user(val):
        username, password = list(map(str, val.split(b";")))
        return User(username, password)
    
    def __new__(self):
        """Handles ensuring that this class is a singleton"""
        if not hasattr(self, 'instance'):
            self.instance = super(Database_Connection, self).__new__(self)
        return self.instance
    
    def __init__(self):
        """Handles initializing the class"""
        self.conn = sqlite3.connect('db/cookbook.db')
        self.cursor = self.conn.cursor()

        # Checking if the tables exist
        userTable = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Users'").fetchone()
        if userTable is None:
            with open("db/createUserTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

    def add_user(self, user: User) -> bool:
        """Adds a new user to the database"""
        try:
            commandString: str = "INSERT INTO Users (Username, Password) VALUES (?, ?)"
            self.cursor.execute(commandString, (user.Username, user.Password,))
            self.conn.commit()

            getIdCommand: str = "SELECT UserId FROM Users WHERE Username = ?"
            self.cursor.execute(getIdCommand, (user.Username,))
            userid: int = self.cursor.fetchone()
            return userid[0]
        except:
            return False
        
    def get_user(self, username: str) -> User:
        """Gets a user based on their username"""
        try: 
            commandString: str = "SELECT * FROM Users WHERE Username = ?"
            self.cursor.execute(commandString, (username,))
            res = self.cursor.fetchone()
            user: User = User(res[1], res[2], res[0])
            return user
        except:
            return None
    
import sqlite3
from datetime import datetime
from db.objects import User, Post

class Database_Connection():
    """Used as a singleton to access the database"""
    
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
        self._ensure_tables_exist()

    def _ensure_tables_exist(self):
        """Ensures that the Users and Posts tables exist in the database"""
        # Check and create Users table if it doesn't exist
        user_table = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Users'").fetchone()
        if user_table is None:
            with open("db/createUserTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        # Check and create Posts table if it doesn't exist
        posts_table = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Posts'").fetchone()
        if posts_table is None:
            with open("db/createPostTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

    def add_user(self, user: User) -> bool:
        """Adds a new user to the database"""
        try:
            command_string: str = "INSERT INTO Users (Username, Password) VALUES (?, ?)"
            self.cursor.execute(command_string, (user.Username, user.Password))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        
    def get_user(self, username: str) -> User:
        """Gets a user based on their username"""
        command_string: str = "SELECT * FROM Users WHERE Username = ?"
        self.cursor.execute(command_string, (username,))
        user_data = self.cursor.fetchone()
        if user_data:
            return User(userId=user_data[0], username=user_data[1], password=user_data[2])
        return None

    def add_post(self, post: Post) -> bool:
        """Adds a new post to the database"""
        try:
            command_string: str = """
                INSERT INTO Posts (UserId, Message, Image, Recipe, Date, Likes, Dislikes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(command_string, (
                post.userId,
                post.message,
                post.image,
                "change",  # to be changed when custom recipes are done
                post.date,
                post.likes,
                post.dislikes,
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding post: {e}")
            return False

    def get_post(self, post_id: int) -> Post:
        """Gets a post based on its postId"""
        command_string: str = "SELECT * FROM Posts WHERE PostId = ?"
        self.cursor.execute(command_string, (post_id,))
        post_data = self.cursor.fetchone()
        if post_data:
            return Post(
                postId=post_data[0],
                userId=post_data[1],
                message=post_data[2],
                image=post_data[3],
                recipe="change",  # to be changed when custom recipes are done
                date=post_data[5],
                likes=post_data[6],
                dislikes=post_data[7],
            )
        return None

    def get_all_posts(self) -> list[Post]:
        """Gets all posts from the database"""
        command_string: str = "SELECT * FROM Posts"
        self.cursor.execute(command_string)
        posts_data = self.cursor.fetchall()
        posts = []
        for post_data in posts_data:
            posts.append(Post(
                postId=post_data[0],
                userId=post_data[1],
                message=post_data[2],
                image=post_data[3],
                recipe="change",  # to be changed when custom recipes are done
                date=post_data[5],
                likes=post_data[6],
                dislikes=post_data[7],
            ))
        return posts

    def update_post_likes(self, post_id: int, likes: int) -> bool:
        """Updates the likes count for a post"""
        try:
            command_string: str = "UPDATE Posts SET Likes = ? WHERE PostId = ?"
            self.cursor.execute(command_string, (likes, post_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating post likes: {e}")
            return False

    def update_post_dislikes(self, post_id: int, dislikes: int) -> bool:
        """Updates the dislikes count for a post"""
        try:
            command_string: str = "UPDATE Posts SET Dislikes = ? WHERE PostId = ?"
            self.cursor.execute(command_string, (dislikes, post_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating post dislikes: {e}")
            return False

    def delete_post(self, post_id: int) -> bool:
        """Deletes a post from the database"""
        try:
            command_string: str = "DELETE FROM Posts WHERE PostId = ?"
            self.cursor.execute(command_string, (post_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False
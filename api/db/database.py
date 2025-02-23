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
        """Ensures that the Users, Posts, and PostReactions tables exist in the database"""
        # Check and create Users table if it doesn't exist
        user_table = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Users'").fetchone()
        if user_table is None:
            with open("db/createUserTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        # Check and create Posts and PostReactions tables if they don't exist
        posts_table = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Posts'").fetchone()
        if posts_table is None:
            with open("db/createPostTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        reactions_table = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='PostReactions'").fetchone()
        if reactions_table is None:
            with open("db/createPostReactionsTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

    def add_user(self, user: User) -> int | bool:
        """Adds a new user to the database, returns UserId on success"""
        try:
            command_string: str = "INSERT INTO Users (Username, Password) VALUES (?, ?)"
            self.cursor.execute(command_string, (user.Username, user.Password))
            self.conn.commit()
            
            getIdCommand: str = "SELECT UserId FROM Users WHERE Username = ?"
            self.cursor.execute(getIdCommand, (user.Username,))
            userid = self.cursor.fetchone()
            return userid[0] if userid else False
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
    
    def get_user_by_id(self, id: int) -> User:
        """Gets a user based on their username"""
        command_string: str = "SELECT * FROM Users WHERE UserId = ?"
        self.cursor.execute(command_string, (id,))
        user_data = self.cursor.fetchone()
        if user_data:
            return User(userId=user_data[0], username=user_data[1], password=user_data[2])
        return None

    def add_post(self, post: Post) -> bool:
        """Adds a new post to the database"""
        try:
            command_string: str = """
                INSERT INTO Posts (UserId, Message, Image, RecipeId, Date)
                VALUES (?, ?, ?, ?, ?)
            """

            if post.recipe is None:
                recipe_id = None  # Use None for NULL in SQLite
            else:
                recipe_id = post.recipe.id

            self.cursor.execute(command_string, (
                post.userId,
                post.message,
                post.image,
                recipe_id,
                post.date,
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding post: {e}")
            return False

    def get_post(self, post_id: int) -> Post:
        """Gets a post based on its postId, including reaction data"""
        command_string: str = "SELECT * FROM Posts WHERE PostId = ?"
        self.cursor.execute(command_string, (post_id,))
        post_data = self.cursor.fetchone()
        if post_data:
            # Fetch likes and dislikes as lists of UserIds
            likes = self.get_post_reactions(post_id, 'LIKE')
            dislikes = self.get_post_reactions(post_id, 'DISLIKE')
            date_value = post_data[5] if post_data[5] is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recipe_value = post_data[4]  # Capture RecipeId
            print(f"RecipeId value: {recipe_value}, type: {type(recipe_value)}")  # Debug type
            return Post(
                postId=post_data[0],
                userId=post_data[1],
                message=post_data[2],
                image=post_data[3],
                recipe=post_data[4],  # To be updated when recipes are implemented
                date=date_value,
                likes=likes,
                dislikes=dislikes,
            )
        return None

    def get_all_posts(self) -> list[Post]:
        """Gets all posts from the database with their reactions"""
        command_string: str = "SELECT * FROM Posts"
        self.cursor.execute(command_string)
        posts_data = self.cursor.fetchall()
        posts = []
        for post_data in posts_data:
            likes = self.get_post_reactions(post_data[0], 'LIKE')
            dislikes = self.get_post_reactions(post_data[0], 'DISLIKE')
            date_value = post_data[5] if post_data[5] is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            posts.append(Post(
                postId=post_data[0],
                userId=post_data[1],
                message=post_data[2],
                image=post_data[3],
                recipe=post_data[4],  # To be updated when recipes are implemented
                date=date_value,
                likes=likes,
                dislikes=dislikes,
            ))
        return posts

    def get_post_reactions(self, post_id: int, reaction_type: str) -> list[int]:
        """Helper method to get list of UserIds for a specific reaction type"""
        command_string: str = "SELECT UserId FROM PostReactions WHERE PostId = ? AND ReactionType = ?"
        self.cursor.execute(command_string, (post_id, reaction_type))
        return [row[0] for row in self.cursor.fetchall()]

    def add_post_reaction(self, post_id: int, user_id: int, reaction_type: str) -> bool:
        """Adds or updates a user's reaction (LIKE or DISLIKE) to a post"""
        try:
            # Check if the user already has a reaction
            check_command: str = "SELECT ReactionType FROM PostReactions WHERE PostId = ? AND UserId = ?"
            self.cursor.execute(check_command, (post_id, user_id))
            existing_reaction = self.cursor.fetchone()

            if existing_reaction:
                # Update existing reaction
                update_command: str = "UPDATE PostReactions SET ReactionType = ? WHERE PostId = ? AND UserId = ?"
                self.cursor.execute(update_command, (reaction_type, post_id, user_id))
            else:
                # Insert new reaction
                insert_command: str = "INSERT INTO PostReactions (PostId, UserId, ReactionType) VALUES (?, ?, ?)"
                self.cursor.execute(insert_command, (post_id, user_id, reaction_type))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding/updating reaction: {e}")
            return False

    def remove_post_reaction(self, post_id: int, user_id: int) -> bool:
        """Removes a user's reaction from a post"""
        try:
            command_string: str = "DELETE FROM PostReactions WHERE PostId = ? AND UserId = ?"
            self.cursor.execute(command_string, (post_id, user_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error removing reaction: {e}")
            return False

    def delete_post(self, post_id: int) -> bool:
        """Deletes a post and its associated reactions from the database"""
        try:
            # Delete reactions first due to foreign key constraints
            self.cursor.execute("DELETE FROM PostReactions WHERE PostId = ?", (post_id,))
            self.cursor.execute("DELETE FROM Posts WHERE PostId = ?", (post_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False
    
    def update_post(self, post_id: int, update_data: dict) -> bool:
        """Updates a post's fields in the database based on provided data."""
        try:
            # Build the SET clause dynamically based on provided fields
            if not update_data:
                return True  # Nothing to update
            
            set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
            command_string = f"UPDATE Posts SET {set_clause} WHERE PostId = ?"
            
            # Add PostId as the last parameter
            values = list(update_data.values()) + [post_id]
            
            self.cursor.execute(command_string, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating post: {e}")
            return False
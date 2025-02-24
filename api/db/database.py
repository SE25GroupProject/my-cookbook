import sqlite3
try:
    from db.objects import User, Recipe, Ingredient, Instruction, Post, Comment
except Exception:
    from objects import User, Recipe, Ingredient, Instruction
from datetime import datetime
from typing import List

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

        # Checking if the tables exist
        recipeTable = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Recipes'").fetchone()
        if recipeTable is None:
            with open("db/createRecipeTable.sql", "r") as sql_file:
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

        # Checking if the tables exist
        userRecipeTable = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='UserRecipes'").fetchone()
        if userRecipeTable is None:
            with open("db/createUserRecipeTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        reactions_table = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='PostReactions'").fetchone()
        if reactions_table is None:
            with open("db/createPostReactionsTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()
        
        # Check and create Comments table
        comments_table = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Comments'").fetchone()
        if comments_table is None:
            with open("db/createCommentsTable.sql", "r") as sql_file:
                self.cursor.executescript(sql_file.read())
                self.conn.commit()

    def add_user(self, user: User) -> int | bool:
        """Adds a new user to the database, returns UserId on success"""
        try:
            getIdCommand: str = "INSERT INTO Users (Username, Password) VALUES (?, ?)"
            self.cursor.execute(getIdCommand, (user.Username, user.Password))
            userid = self.cursor.fetchone()
            return userid[0] if userid else False
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        
    def get_user_by_name(self, username: str) -> User:
        """Gets a user based on their username"""
        try: 
            commandString: str = "SELECT * FROM Users WHERE Username = ?"
            self.cursor.execute(commandString, (username,))
            res = self.cursor.fetchone()
            user: User = User(res[1], res[2], res[0])
            return user
        except:
            return None
        
    def get_user_by_id(self, userId: int) -> User:
        """Gets a user based on their username"""
        try: 
            commandString: str = "SELECT * FROM Users WHERE userId = ?"
            self.cursor.execute(commandString, (userId,))
            res = self.cursor.fetchone()
            user: User = User(res[1], res[2], res[0])
            return user
        except:
            return None
        
    def create_recipe(self, recipe: Recipe, userId: int):
        """Creates a recipe based on the object provided"""
        try:
            commandString: str = """INSERT INTO Recipes (name, cookTime, prepTime, totalTime, description, category, rating, calories, fat, saturatedFat, cholesterol, sodium, carbs, fiber, sugar, protein, servings)   
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            
            self.cursor.execute(commandString, (recipe.Name, recipe.CookTime, recipe.PrepTime, recipe.TotalTime, recipe.Description, 
                                                recipe.Category, recipe.Rating, recipe.Calories, recipe.Fat, recipe.SaturatedFat, 
                                                recipe.Cholesterol, recipe.Sodium, recipe.Carbs, recipe.Fiber, recipe.Sugar, recipe.Protein, recipe.Servings,))
            
            
            recipeId: int = self.cursor.lastrowid

            for image in recipe.Images:
                commandString: str = """INSERT INTO Images (recipeId, imageUrl) VALUES (?, ?)"""
                self.cursor.execute(commandString, (recipeId, image,))

            for tag in recipe.Tags:
                commandString: str = """INSERT INTO Tags (recipeId, tag) VALUES (?, ?)"""
                self.cursor.execute(commandString, (recipeId, tag,))

            for ingredient in recipe.Ingredients:
                commandString: str = """INSERT INTO Ingredients (recipeId, name, amount) VALUES (?, ?, ?)"""
                self.cursor.execute(commandString, (recipeId, ingredient.Name, ingredient.Amount,))

            for instructions in recipe.Instructions:
                commandString: str = """INSERT INTO Instructions (recipeId, step, instruction) VALUES (?, ?, ?)"""
                self.cursor.execute(commandString, (recipeId, instructions.Step, instructions.Instruction,))

            commandString: str = """INSERT INTO UserRecipes (recipeId, userId) VALUES (?, ?)"""
            self.cursor.execute(commandString, (recipeId, userId,))

            self.conn.commit()
            return recipeId

        except Exception as e:
            print(e)
            return False
        
    def get_recipe(self, recipeId: int):
        """Gets a recipe based on its id"""
        try:
            commandString: str = """SELECT * FROM Recipes WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            recipeRes = self.cursor.fetchone()

            commandString: str = """SELECT * FROM Images WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            imagesRes = self.cursor.fetchall()
            imageList: list[str] = []
            for image in imagesRes:
                imageList.append(image[1])

            commandString: str = """SELECT * FROM Tags WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            tagsRes = self.cursor.fetchall()
            tagsList: list[str] = []
            for tag in tagsRes:
                tagsList.append(tag[1])

            commandString: str = """SELECT * FROM Ingredients WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            ingredientsRes = self.cursor.fetchall()
            ingredientsList: list[Ingredient] = []
            for _, ingredient, amount in ingredientsRes:
                ingredientsList.append(Ingredient(ingredient, amount))

            commandString: str = """SELECT * FROM Instructions WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            instructionsRes = self.cursor.fetchall()
            instructionsList: list[Instruction] = []
            for _, step, instruction in instructionsRes:
                instructionsList.append(Instruction(step, instruction))

            recipe: Recipe = Recipe(recipeRes[1], recipeRes[2], recipeRes[3], recipeRes[4], recipeRes[5], recipeRes[6], recipeRes[7], 
                recipeRes[8], recipeRes[9], recipeRes[10], recipeRes[11], recipeRes[12], recipeRes[13], recipeRes[14], recipeRes[15],
                recipeRes[16], recipeRes[17], imageList, tagsList, ingredientsList, instructionsList)

            return recipe
        
        except Exception as e:
            print(e)
            return None
    
    def update_recipe(self, oldRecipeId: int, newRecipe: Recipe):
        """Updates a recipe to have the data of the new recipe"""
        recipe_owner: int = self.get_recipe_owner_by_recipeId(oldRecipeId)
        self.delete_recipe(oldRecipeId)
        self.create_recipe(newRecipe, recipe_owner)

    def delete_recipe(self, recipeId: int):
        """Deletes a recipe from the db"""
        try:
            commandString: str = """DELETE FROM Recipes WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            return True
        
        except Exception as e:
            print(e)
            return False
        
    def get_recipe_owner_by_recipeId(self, recipeId: int):
        """Gets the owner of the recipe"""
        try:
            commandString: str = """SELECT userId FROM UserRecipes WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            res = self.cursor.fetchone()
            userId = res[0]
            user: User = self.get_user_by_id(userId)
            return user
        except Exception as e:
            print(e)
            return None
        
    def get_recipes_owned_by_userId(self, userId: int):
        """Gets the owner of the recipe"""
        try:
            commandString: str = """SELECT recipeId FROM UserRecipes WHERE userId = ?"""
            self.cursor.execute(commandString, (userId,))
            res = self.cursor.fetchall()
            return res
        
        except Exception as e:
            print(e)
            return None
        
    def unfavorite_recipe(self, userId: int, recipeId: int):
        """Unfavorites a recipe"""
        try:
            commandString: str = """DELETE FROM UserFavorites WHERE recipeId = ? AND userId = ?"""
            self.cursor.execute(commandString, (recipeId, userId,))
            return True
        
        except Exception as e:
            print(e)
            return False
        
    def favorite_recipe(self, userId: int, recipeId: int):
        """Favorites a recipe"""
        try:
            commandString: str = """INSERT INTO UserFavorites (recipeId, userId) VALUES (?, ?)"""
            self.cursor.execute(commandString, (recipeId, userId,))
            return True
        
        except Exception as e:
            print(e)
            return False
        
    def get_favorite_recipes(self, userId: int):
        """Gets someones favorite recipes"""
        try:
            commandString: str = """SELECT * FROM UserFavorites WHERE userId = ?"""
            self.cursor.execute(commandString, (userId,))
            res = self.cursor.fetchall()
            return res
        
        except Exception as e:
            print(e)
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
        try:
            command_string = "INSERT INTO Posts (UserId, Message, Image, RecipeId, Date) VALUES (?, ?, ?, ?, ?)"
            recipe_id = post.recipe  # Already an int or None
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
        """Gets a post based on its postId, including reaction and comment data"""
        command_string = "SELECT PostId, UserId, Message, Image, RecipeId, Date FROM Posts WHERE PostId = ?"
        self.cursor.execute(command_string, (post_id,))
        post_data = self.cursor.fetchone()
        if post_data:
            likes = self.get_post_reactions(post_id, 'LIKE')
            dislikes = self.get_post_reactions(post_id, 'DISLIKE')
            comments = self.get_post_comments(post_id)  # Fetch comments
            date_value = post_data[5] if post_data[5] is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recipe_value = post_data[4]
            if recipe_value is not None:
                try:
                    recipe_value = int(recipe_value)
                except (ValueError, TypeError):
                    recipe_value = None
            return Post(
                postId=post_data[0],
                userId=post_data[1],
                message=post_data[2],
                image=post_data[3],
                recipe=recipe_value,
                date=date_value,
                likes=likes,
                dislikes=dislikes,
                comments=comments,
            )
        return None

    def get_all_posts(self) -> list[Post]:
        """Gets all posts from the database with their reactions and comments"""
        command_string = "SELECT PostId, UserId, Message, Image, RecipeId, Date FROM Posts"
        self.cursor.execute(command_string)
        posts_data = self.cursor.fetchall()
        posts = []
        for post_data in posts_data:
            likes = self.get_post_reactions(post_data[0], 'LIKE')
            dislikes = self.get_post_reactions(post_data[0], 'DISLIKE')
            comments = self.get_post_comments(post_data[0])  # Fetch comments
            date_value = post_data[5] if post_data[5] is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recipe_value = post_data[4]
            if recipe_value is not None:
                try:
                    recipe_value = int(recipe_value)
                except (ValueError, TypeError):
                    recipe_value = None
            posts.append(Post(
                postId=post_data[0],
                userId=post_data[1],
                message=post_data[2],
                image=post_data[3],
                recipe=recipe_value,
                date=date_value,
                likes=likes,
                dislikes=dislikes,
                comments=comments,
            ))
        return posts

    def get_post_reactions(self, post_id: int, reaction_type: str) -> list[int]:
        command_string = "SELECT UserId FROM PostReactions WHERE PostId = ? AND ReactionType = ?"
        self.cursor.execute(command_string, (post_id, reaction_type))
        return [row[0] for row in self.cursor.fetchall()]

    def add_post_reaction(self, post_id: int, user_id: int, reaction_type: str) -> bool:
        try:
            check_command = "SELECT ReactionType FROM PostReactions WHERE PostId = ? AND UserId = ?"
            self.cursor.execute(check_command, (post_id, user_id))
            existing_reaction = self.cursor.fetchone()
            if existing_reaction:
                update_command = "UPDATE PostReactions SET ReactionType = ? WHERE PostId = ? AND UserId = ?"
                self.cursor.execute(update_command, (reaction_type, post_id, user_id))
            else:
                insert_command = "INSERT INTO PostReactions (PostId, UserId, ReactionType) VALUES (?, ?, ?)"
                self.cursor.execute(insert_command, (post_id, user_id, reaction_type))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding/updating reaction: {e}")
            return False

    def remove_post_reaction(self, post_id: int, user_id: int) -> bool:
        try:
            command_string = "DELETE FROM PostReactions WHERE PostId = ? AND UserId = ?"
            self.cursor.execute(command_string, (post_id, user_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error removing reaction: {e}")
            return False

    def delete_post(self, post_id: int) -> bool:
        """Deletes a post and its associated reactions and comments from the database"""
        try:
            # Delete reactions and comments first due to foreign key constraints
            self.cursor.execute("DELETE FROM PostReactions WHERE PostId = ?", (post_id,))
            self.cursor.execute("DELETE FROM Comments WHERE PostId = ?", (post_id,))
            self.cursor.execute("DELETE FROM Posts WHERE PostId = ?", (post_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False
    
    def update_post(self, post_id: int, update_data: dict) -> bool:
        try:
            if not update_data:
                return True
            set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
            command_string = f"UPDATE Posts SET {set_clause} WHERE PostId = ?"
            values = list(update_data.values()) + [post_id]
            self.cursor.execute(command_string, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating post: {e}")
            return False

    def add_comment(self, comment: Comment) -> int | bool:
            """Adds a new comment to a post and returns the CommentId"""
            try:
                command_string = "INSERT INTO Comments (PostId, UserId, Message, Date) VALUES (?, ?, ?, ?)"
                self.cursor.execute(command_string, (
                    comment.postId,
                    comment.userId,
                    comment.message,
                    comment.date or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  
                ))
                self.conn.commit()

                self.cursor.execute("SELECT last_insert_rowid()")
                comment_id = self.cursor.fetchone()[0]
                return comment_id
            except Exception as e:
                print(f"Error adding comment: {e}")
                return False

    def get_post_comments(self, post_id: int) -> List[Comment]:
        """Fetches all comments for a given post"""
        try:
            command_string = "SELECT CommentId, UserId, PostId, Message, Date FROM Comments WHERE PostId = ?"
            self.cursor.execute(command_string, (post_id,))
            comments_data = self.cursor.fetchall()
            return [Comment(
                commentId=row[0],
                userId=row[1],
                postId=row[2],
                message=row[3],
                date=row[4] if row[4] is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ) for row in comments_data]
        except Exception as e:
            print(f"Error fetching comments: {e}")
            return []

    def delete_comment(self, comment_id: int) -> bool:
        """Deletes a comment by its CommentId"""
        try:
            command_string = "DELETE FROM Comments WHERE CommentId = ?"
            self.cursor.execute(command_string, (comment_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting comment: {e}")
            return False

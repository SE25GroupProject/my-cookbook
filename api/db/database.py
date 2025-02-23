"""Used to hold the information about the database and commands used with it"""

import sqlite3
try:
    from db.objects import User, Recipe, Ingredient, Instruction
except Exception:
    from objects import User, Recipe, Ingredient, Instruction

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
        self.conn = sqlite3.connect('cookbook.db')
        self.cursor = self.conn.cursor()

        # Checking if the tables exist
        userTable = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Users'").fetchone()
        if userTable is None:
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

        # Checking if the tables exist
        userRecipeTable = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='UserRecipes'").fetchone()
        if userRecipeTable is None:
            with open("db/createUserRecipeTable.sql", "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()


    def add_user(self, user: User) -> bool:
        """Adds a new user to the database"""
        try:
            commandString: str = "INSERT INTO Users (Username, Password) VALUES (?, ?)"
            self.cursor.execute(commandString, (user.Username, user.Password,))
            self.conn.commit()

            return self.cursor.lastrowid
        except:
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

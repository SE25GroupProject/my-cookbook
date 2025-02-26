import sqlite3
from typing import List
from api.models import MealPlanEntry, RecipeListEntry, ShoppingListItem, Post, Comment, PostRecipe, Recipe, Instruction

try:
    from api.db.objects import User, Ingredient
except sqlite3.DatabaseError:
    from db.objects import User, Ingredient
from datetime import datetime

class Database_Connection():
    def __init__(self, dbPath: str = 'db/cookbook.db'):
        """Handles initializing the class"""
        self.conn = sqlite3.connect(dbPath, check_same_thread=False)
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

        # Checking if the Meal Plan table exist
        mealPlanTable = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='MealPlan'").fetchone()
        shoppingTable = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='ShoppingList'").fetchone()
        if mealPlanTable is None or shoppingTable is None: 
            with open("db/createMealPrepTable.sql", "r") as sql_file:
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

    # ------------------------------------------------------
    # User Interactions
    # ------------------------------------------------------

    def add_user(self, user: User) -> int | bool:
        """Adds a new user to the database, returns UserId on success"""
        try:
            getIdCommand: str = "INSERT INTO Users (Username, Password) VALUES (?, ?)"
            self.cursor.execute(getIdCommand, (user.Username, user.Password))
            self.conn.commit()
            return self.get_user_by_name(user.Username).UserId
        except sqlite3.DatabaseError as e:
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
        
    def get_user_by_name2(self, username: str) -> User:
        """Gets a user based on their username"""
        try: 
            commandString: str = "SELECT * FROM Users"
            self.cursor.execute(commandString)
            res = self.cursor.fetchall()
            # user: User = User(res[1], res[2], res[0])
            # return user
            return res
        except:
            return None


    
    def get_user_by_id(self, id: int) -> User:
        """Gets a user based on their username"""
        # print( id)
        command_string: str = "SELECT * FROM Users WHERE UserId = ?"
        self.cursor.execute(command_string, (id,))
        user_data = self.cursor.fetchone()

        # print(user_data)
        if user_data:
            return User(userId=user_data[0], username=user_data[1], password=user_data[2])
        return None

    # ------------------------------------------------------
    # User Recipe Interactions
    # ------------------------------------------------------
        
    def create_recipe(self, recipe: Recipe, userId: int):
        """Creates a recipe based on the object provided"""
        try:
            commandString: str = """INSERT INTO Recipes (name, cookTime, prepTime, totalTime, description, category, rating, calories, fat, saturatedFat, cholesterol, sodium, carbs, fiber, sugar, protein, servings)   
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            
            self.cursor.execute(commandString, (recipe.name, recipe.cookTime, recipe.prepTime, recipe.totalTime, recipe.description, 
                                                recipe.category, recipe.rating, recipe.calories, recipe.fat, recipe.saturatedFat, 
                                                recipe.cholesterol, recipe.sodium, recipe.carbs, recipe.fiber, recipe.sugar, recipe.protein, recipe.servings,))
            
            
            recipeId: int = self.cursor.lastrowid

            # print("images")
            for image in recipe.images:
                commandString: str = """INSERT INTO Images (recipeId, imageUrl) VALUES (?, ?)"""
                self.cursor.execute(commandString, (recipeId, image,))
            # print("tags")

            for tag in recipe.tags:
                commandString: str = """INSERT INTO Tags (recipeId, tag) VALUES (?, ?)"""
                self.cursor.execute(commandString, (recipeId, tag,))
            # print("ing")

            for ingredient in recipe.ingredients:
                commandString: str = """INSERT INTO Ingredients (recipeId, name, amount) VALUES (?, ?, ?)"""
                self.cursor.execute(commandString, (recipeId, ingredient, 0,))
            # print("inst")

            for instructions in recipe.instructions:
                commandString: str = """INSERT INTO Instructions (recipeId, step, instruction) VALUES (?, ?, ?)"""
                self.cursor.execute(commandString, (recipeId, instructions.step, instructions.instruction,))

            commandString: str = """INSERT INTO UserRecipes (recipeId, userId) VALUES (?, ?)"""
            self.cursor.execute(commandString, (recipeId, userId,))

            self.conn.commit()
            return recipeId

        except sqlite3.DatabaseError as e:
            print(e)
            return False
    
    def testing(self):
        try:
            commandString: str = """SELECT recipeId FROM Recipes"""
            self.cursor.execute(commandString)
            recipeRes = self.cursor.fetchone()
            if not recipeRes:
                print("No recipe value found.")
                return None
            
            print("Recipe Res")
        
        except sqlite3.DatabaseError as e:
            print(e)
            return None
        

        
    def get_recipe(self, recipeId: int):
        """Gets a recipe based on its id"""
        try:
            commandString: str = """SELECT * FROM Recipes WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            recipeRes = self.cursor.fetchone()
            if not recipeRes:
                print("No recipe value found.")
                return None
            
            # print(recipeRes)
        

            commandString: str = """SELECT * FROM Images WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            imagesRes = self.cursor.fetchall()
            imageList: list[str] = []
            for image in imagesRes:
                imageList.append(image[1])


            # print("got images")
            commandString: str = """SELECT * FROM Tags WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            tagsRes = self.cursor.fetchall()
            tagsList: list[str] = []
            for tag in tagsRes:
                tagsList.append(tag[1])

            # print("got tags")
            commandString: str = """SELECT * FROM Ingredients WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            ingredientsRes = self.cursor.fetchall()
            ingredientsList: list[str] = []
            for _, ingredient, amount in ingredientsRes:
                ingredientsList.append(ingredient)
            # print("got ingredients")
            commandString: str = """SELECT * FROM Instructions WHERE recipeId = ?"""
            self.cursor.execute(commandString, (recipeId,))
            instructionsRes = self.cursor.fetchall()
            instructionsList: list[Instruction] = []
            for _, step, instruction in instructionsRes:
                instructionsList.append(Instruction(step = step, instruction = instruction))

            # print(instructionsList)
            recipe: Recipe = Recipe(recipeId = recipeRes[0], name = recipeRes[1], cookTime = recipeRes[2], 
                                    prepTime = recipeRes[3], totalTime = recipeRes[4], description = recipeRes[5],
                                    category = recipeRes[6], rating = recipeRes[7], calories = recipeRes[8], 
                                    fat = recipeRes[9], saturatedFat = recipeRes[10], cholesterol = recipeRes[11], 
                                    sodium = recipeRes[12], carbs = recipeRes[13], fiber = recipeRes[14], sugar = recipeRes[15],
                                    protein = recipeRes[16], servings = recipeRes[17], images = imageList, tags = tagsList, 
                                    ingredients = ingredientsList, instructions = instructionsList)

            return recipe
        
        except sqlite3.DatabaseError as e:
            print(e)
            return None
    

    def get_recipe_batch(self, recipeIds: List[int], fullRecipe: bool = False):
        try: 
            recipes = []
            if fullRecipe: 
                for recipeid in recipeIds:
                    recipes.append(self.get_recipe(recipeid))
            else: 
                commandString: str = """SELECT * FROM Recipes WHERE recipeId IN (%s)"""%','.join('?'*len(recipeIds))
                self.cursor.execute(commandString, (*recipeIds,))
                recipeObjs = self.cursor.fetchall()
                if not recipeObjs:
                    print("No recipe values found.")
                    return []

                
                for recipe in recipeObjs:
                    recipes.append(RecipeListEntry(name=recipe[1], cookTime=recipe[2], prepTime=recipe[3], totalTime=recipe[4], 
                                        description=recipe[5], category=recipe[6], rating=recipe[7], calories=recipe[8], 
                                        fat=recipe[9], saturatedFat=recipe[10], cholesterol=recipe[11], sodium=recipe[12], 
                                        carbs=recipe[13], fiber=recipe[14], sugar=recipe[15], protein=recipe[16], 
                                        servings=recipe[17], recipeId=recipe[0]))

            return recipes

        except sqlite3.DatabaseError as e: 
            print(e)
            return []

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
        
        except sqlite3.DatabaseError as e:
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
        except sqlite3.DatabaseError as e:
            print(e)
            return None
        
    def get_recipes_owned_by_userId(self, userId: int):
        """Gets the owner of the recipe"""
        try:
            commandString: str = """SELECT recipeId FROM UserRecipes WHERE userId = ?"""
            self.cursor.execute(commandString, (userId,))
            res = self.cursor.fetchall()
            return res
        
        except sqlite3.DatabaseError as e:
            print(e)
            return None
        
    # ------------------------------------------------------
    # Favorite Recipe Interactions
    # ------------------------------------------------------

    def unfavorite_recipe(self, userId: int, recipeId: int):
        """Unfavorites a recipe"""
        try:
            commandString: str = """DELETE FROM UserFavorites WHERE recipeId = ? AND userId = ?"""
            self.cursor.execute(commandString, (recipeId, userId,))
            self.conn.commit()
            return True
        
        except sqlite3.DatabaseError as e:
            print(e)
            return False
        
    def favorite_recipe(self, userId: int, recipeId: int):
        """Favorites a recipe"""
        try:
            commandString: str = """INSERT INTO UserFavorites (recipeId, userId) VALUES (?, ?)"""
            self.cursor.execute(commandString, (recipeId, userId,))
            self.conn.commit()
            return True
        
        except sqlite3.DatabaseError as e:
            print(e)
            return False
        
    def get_favorite_recipes(self, userId: int):
        """Gets someones favorite recipes"""
        try:
            commandString: str = """SELECT recipeId FROM UserFavorites WHERE userId = ?"""
            self.cursor.execute(commandString, (userId,))
            res = self.cursor.fetchall()
            return res
        
        except sqlite3.DatabaseError as e:
            print(e)
            return None
    
    def check_is_favorited(self, recipeId: int, userId: int):
        """Checks to see whether a user has liked a particular post"""
        try: 
            commandString: str = """SELECT * FROM UserFavorites WHERE recipeId = ? AND userId = ?;"""
            self.cursor.execute(commandString, (recipeId, userId,))
            res = self.cursor.fetchone()
            if(res): return True
            return False
            
        except sqlite3.DatabaseError as e: 
            print(e)
            return False

    # ------------------------------------------------------
    # Recipe Search Interactions
    # ------------------------------------------------------
    
    def get_count_recipes_by_ingredients(self, ings: List[str], ):
        try:
            countCommand: str = """SELECT recipeId FROM (SELECT DISTINCT name, recipeId FROM ingredients WHERE name IN (%s)) GROUP BY recipeId HAVING COUNT(name) >= ? ;""" %','.join('?'*len(ings))
            res = self.cursor.execute(countCommand, (*ings, len(ings), ))
            count = len(res.fetchall())
            return count
        except sqlite3.DatabaseError as e: 
            print(e)
            return -1
        
    def get_recipes_by_ingredient(self, ings: List[str], page: int, per_page: int = 10):
        """Retrieves a list of recipe ids containing the given ingredients limited by the number per page"""
        try:
            commandString: str = """SELECT recipeId FROM (SELECT DISTINCT name, recipeId FROM ingredients WHERE name IN (%s)) GROUP BY recipeId HAVING COUNT(name) >= ? LIMIT ? OFFSET ?;""" %','.join('?'*len(ings))
            res = self.cursor.execute(commandString, (*ings, len(ings), per_page, page * per_page ))
            recipeIds = (*res.fetchall(),)

            recipeCommand: str = """SELECT * FROM recipes WHERE recipeId IN (%s)"""%','.join('?'*len(recipeIds))
            res = self.cursor.execute(recipeCommand, tuple(id for recipeRecord in recipeIds for id in recipeRecord))

            recipeObjs = res.fetchall()

            recipes = []
            for recipe in recipeObjs:
                recipes.append(RecipeListEntry(name=recipe[1], cookTime=recipe[2], prepTime=recipe[3], totalTime=recipe[4], 
                                    description=recipe[5], category=recipe[6], rating=recipe[7], calories=recipe[8], 
                                    fat=recipe[9], saturatedFat=recipe[10], cholesterol=recipe[11], sodium=recipe[12], 
                                    carbs=recipe[13], fiber=recipe[14], sugar=recipe[15], protein=recipe[16], 
                                    servings=recipe[17], recipeId=recipe[0]))

            print(recipes)
            return recipes
        except sqlite3.DatabaseError as e: 
            print(e)
            return[]
        
    def get_count_recipes_by_nutrition(self, caloriesMax: int, fatMax: int, sugMax: int, proMax: int, ):
        try:
            countCommand: str = """SELECT * FROM recipes WHERE calories <= ? AND fat <= ? AND sugar <= ? and protein <= ? ;""" 
            res = self.cursor.execute(countCommand, (caloriesMax, fatMax, sugMax, proMax,))

            count = len(res.fetchall())
            return count
        except sqlite3.DatabaseError as e: 
            print(e)
            return -1

    def get_recipes_by_nutrition(self, caloriesMax: int, fatMax: int, sugMax: int, proMax: int, page: int, per_page: int = 10):
        """Retrieves a list of recipe ids containing the given ingredients limited by the number per page"""
        try:
            commandString: str = """SELECT * FROM recipes WHERE calories <= ? AND fat <= ? AND sugar <= ? and protein <= ? LIMIT ? OFFSET ?; """
            print(commandString)
            res = self.cursor.execute(commandString, (caloriesMax, fatMax, sugMax, proMax, per_page, page * per_page,))

            recipeObjs = res.fetchall()

            recipes = []
            for recipe in recipeObjs:
                recipes.append(RecipeListEntry(name=recipe[1], cookTime=recipe[2], prepTime=recipe[3], totalTime=recipe[4], 
                                    description=recipe[5], category=recipe[6], rating=recipe[7], calories=recipe[8], 
                                    fat=recipe[9], saturatedFat=recipe[10], cholesterol=recipe[11], sodium=recipe[12], 
                                    carbs=recipe[13], fiber=recipe[14], sugar=recipe[15], protein=recipe[16], 
                                    servings=recipe[17], recipeId=recipe[0]))

            return recipes
        except sqlite3.DatabaseError as e: 
            print(e)
            return[]
        
    def get_ingredient_list(self, ing: str): 
        try: 
            commandString: str = """SELECT name FROM ingredients WHERE name LIKE ? GROUP BY name LIMIT 10;"""
            res = self.cursor.execute(commandString, (f"%{ing}%", ))

            return res.fetchall()
        except sqlite3.DatabaseError as e: 
                print(e)
                return[]
    
    # ------------------------------------------------------
    # Meal Plan Interactions
    # ------------------------------------------------------

    def get_user_meal_plan(self, UserId: int):
        try:
            commandString: str = "SELECT * FROM MealPlan WHERE userId = ?;"
            mealplan = self.cursor.execute(commandString, (UserId,)).fetchall()
            formattedPlan = [ MealPlanEntry(day=mealitem[2], recipe={"recipeId": mealitem[1]}) for mealitem in mealplan]

            for entry in formattedPlan:
                entry.recipe.name = self.cursor.execute("SELECT name FROM recipes WHERE recipeId = ? ;", (entry.recipe.recipeId,)).fetchone()[0]

            return formattedPlan
        except sqlite3.DatabaseError as e:
            print(e)
            return []

    def update_user_meal_plan(self, UserId: int, day: int, recipeId:int):
        try: 
            commandString: str = "INSERT INTO MealPlan(userId,recipeId,dayOfWeek) VALUES (?,?,?) ON CONFLICT(userId, dayOfWeek) DO UPDATE SET recipeId = excluded.recipeId;"
            self.cursor.execute(commandString, (UserId, recipeId, day))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            print(e)
            return f"There was an error with updating the meal plan of user {UserId} for the day {day}"
    
    def remove_from_user_meal_plan(self, UserId: int, day: int):
        try: 
            exists = self.cursor.execute("SELECT * FROM MealPlan WHERE userId = ? AND dayOfWeek = ?;", (UserId, day)).fetchone
            if (exists is None):
                return f"An isntance with userId of {UserId} and day of {day} does not exist in the database."
            
            commandString: str = "DELETE FROM MealPlan WHERE userId = ? AND dayOfWeek = ?"
            self.cursor.execute(commandString, (UserId, day))
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            print(e)
            return f"There was an error removing the instance with userId of {UserId} and day of {day} from the database."
    
    # ------------------------------------------------------
    # Shopping List Interactions
    # ------------------------------------------------------

    def get_user_shopping_list(self, UserId: int):
        try:
            commandString: str = "SELECT * FROM ShoppingList WHERE userId = ?;"
            shoppingList = self.cursor.execute(commandString, (UserId,)).fetchall()
            formattedList = [ShoppingListItem(name=shoppingItem[1], quantity=shoppingItem[2], unit=shoppingItem[3], checked=shoppingItem[4]) for shoppingItem in shoppingList]
            return formattedList
        except sqlite3.DatabaseError as e:
            print(e)
            return[]
        
    def update_shopping_list_item(self, UserId: int, name: str, quantity: int, unit: str, checked: bool):
        try: 
            commandString: str = "INSERT INTO ShoppingList(userId,name,quantity,unit,checked) VALUES (?,?,?,?,?) ON CONFLICT(userId, name) DO UPDATE SET quantity = excluded.quantity, unit = excluded.unit, checked = excluded.checked;"
            self.cursor.execute(commandString, (UserId, name, quantity, unit, 1 if checked else 0,))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            print(e)
            return f"There was an error with updating the shopping list of user {UserId} for the item {name}"
        
    def remove_from_shopping_list(self, UserId: int, name: str):
        try: 
            exists = self.cursor.execute("SELECT * FROM ShoppingList WHERE userId = ? AND name = ?;", (UserId, name)).fetchone()
            if (exists is None):
                return f"An instance with userId of {UserId} and name of {name} does not exist in the database."

            commandString: str = "DELETE FROM ShoppingList WHERE userId = ? AND name = ?;"
            self.cursor.execute(commandString, (UserId, name))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            print(e)
            return f"There was an error removing the instance with userId of {UserId} and name of {name} from the database."

    # ------------------------------------------------------
    # Post Interactions
    # ------------------------------------------------------

    def add_post(self, post: Post) -> bool:
        try:
            command_string = "INSERT INTO Posts (UserId, Message, Image, RecipeId, Date) VALUES (?, ?, ?, ?, ?)"
            if post.recipe is not None:
                recipe_id = post.recipe.recipeId  # Already an int or None
            else:
                recipe_id = None
            self.cursor.execute(command_string, (
                post.userId,
                post.message,
                post.image,
                recipe_id,
                post.date,
            ))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
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
                comments = self.get_post_comments(post_id)
                date_value = post_data[5] if post_data[5] is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                recipe_id = post_data[4]
                recipe_obj = None  
                if recipe_id is not None:
                    try:
                        recipe_id = int(recipe_id)
                        result = self.cursor.execute("SELECT name FROM recipes WHERE recipeId = ?;", (recipe_id,)).fetchone()
                        if result:
                            recipe_name = result[0]
                            recipe_obj = PostRecipe(recipeId=recipe_id, name=recipe_name)
                    except (ValueError, TypeError, IndexError):
                        pass  # recipe_obj stays None

                return Post(
                    postId=post_data[0],
                    userId=post_data[1],
                    message=post_data[2],
                    image=post_data[3],
                    recipe=recipe_obj,
                    date=date_value,
                    likes=likes,
                    dislikes=dislikes,
                    comments=comments,
                )
            return None

    def get_all_posts(self) -> List[Post]:
        """Gets all posts from the database with their reactions and comments"""
        command_string = "SELECT PostId, UserId, Message, Image, RecipeId, Date FROM Posts"
        self.cursor.execute(command_string)
        posts_data = self.cursor.fetchall()
        posts = []
        for post_data in posts_data:
            likes = self.get_post_reactions(post_data[0], 'LIKE')
            dislikes = self.get_post_reactions(post_data[0], 'DISLIKE')
            comments = self.get_post_comments(post_data[0])
            date_value = post_data[5] if post_data[5] is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recipe_id = post_data[4]
            recipe_obj = None  
            if recipe_id is not None:
                try:
                    recipe_id = int(recipe_id)
                    result = self.cursor.execute("SELECT name FROM recipes WHERE recipeId = ?;", (recipe_id,)).fetchone()
                    if result:
                        recipe_name = result[0]
                        recipe_obj = PostRecipe(recipeId=recipe_id, name=recipe_name)
                except (ValueError, TypeError, IndexError):
                    pass  # recipe_obj stays None

            posts.append(Post(
                postId=post_data[0],
                userId=post_data[1],
                message=post_data[2],
                image=post_data[3],
                recipe=recipe_obj,
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
        except sqlite3.DatabaseError as e:
            print(f"Error adding/updating reaction: {e}")
            return False

    def remove_post_reaction(self, post_id: int, user_id: int) -> bool:
        try:
            command_string = "DELETE FROM PostReactions WHERE PostId = ? AND UserId = ?"
            self.cursor.execute(command_string, (post_id, user_id))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
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
        except sqlite3.DatabaseError as e:
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
        except sqlite3.DatabaseError as e:
            print(f"Error updating post: {e}")
            return False

    # ------------------------------------------------------
    # Post Comment Interactions
    # ------------------------------------------------------

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
            except sqlite3.DatabaseError as e:
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
        except sqlite3.DatabaseError as e:
            print(f"Error fetching comments: {e}")
            return []

    def delete_comment(self, comment_id: int) -> bool:
        """Deletes a comment by its CommentId"""
        try:
            command_string = "DELETE FROM Comments WHERE CommentId = ?"
            self.cursor.execute(command_string, (comment_id,))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            print(f"Error deleting comment: {e}")
            return False

"""Class for handling db connections"""

import sqlite3
from typing import List
from datetime import datetime
from api.models import MealPlanEntry, RecipeListEntry, ShoppingListItem
from api.models import Post, Comment, PostRecipe, Recipe, Instruction

try:
    from api.db.objects import User
except ImportError:
    from db.objects import User

# pylint: disable=C0301


class DatabaseConnection:
    """Class for handling the connection"""

    def __init__(self, db_path: str = "db/cookbook.db"):
        """Handles initializing the class"""
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Checking if the tables exist
        self._ensure_tables_exist()

    def _ensure_tables_exist(self):
        """Ensures that the Users, Posts, and PostReactions tables exist in the database"""
        # Check and create Users table if it doesn't exist
        cmd: str = (
            """SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Users'"""
        )
        user_table = self.cursor.execute(cmd).fetchone()
        if user_table is None:
            with open("db/createUserTable.sql", "r", encoding="utf-8") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        # Checking if the tables exist
        cmd: str = (
            "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Recipes'"
        )
        recipe_table = self.cursor.execute(cmd).fetchone()
        if recipe_table is None:
            with open("db/createRecipeTable.sql", "r", encoding="utf-8") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        # Check and create Posts and PostReactions tables if they don't exist
        cmd: str = (
            "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Posts'"
        )
        posts_table = self.cursor.execute(cmd).fetchone()
        if posts_table is None:
            with open("db/createPostTable.sql", "r", encoding="utf-8") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        # Checking if the Meal Plan table exist
        cmd: str = (
            "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='MealPlan'"
        )
        meal_plan_table = self.cursor.execute(cmd).fetchone()

        cmd = "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='ShoppingList'"
        shopping_table = self.cursor.execute(cmd).fetchone()
        if meal_plan_table is None or shopping_table is None:
            with open("db/createMealPrepTable.sql", "r", encoding="utf-8") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        # Checking if the tables exist
        cmd = "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='UserRecipes'"
        user_recipe_table = self.cursor.execute(cmd).fetchone()
        if user_recipe_table is None:
            with open(
                "db/createUserRecipeTable.sql", "r", encoding="utf-8"
            ) as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        cmd = "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='PostReactions'"
        reactions_table = self.cursor.execute(cmd).fetchone()
        if reactions_table is None:
            with open(
                "db/createPostReactionsTable.sql", "r", encoding="utf-8"
            ) as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()

        # Check and create Comments table
        cmd = "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='Comments'"
        comments_table = self.cursor.execute(cmd).fetchone()
        if comments_table is None:
            with open("db/createCommentsTable.sql", "r", encoding="utf-8") as sql_file:
                self.cursor.executescript(sql_file.read())
                self.conn.commit()

    # ------------------------------------------------------
    # User Interactions
    # ------------------------------------------------------

    def add_user(self, user: User) -> int | bool:
        """Adds a new user to the database, returns UserId on success"""
        try:
            get_id_command: str = "INSERT INTO Users (Username, Password) VALUES (?, ?)"
            self.cursor.execute(get_id_command, (user.Username, user.Password))
            self.conn.commit()
            return self.get_user_by_name(user.Username).UserId
        except sqlite3.DatabaseError as e:
            print(f"Error adding user: {e}")
            return False

    def get_user_by_name(self, username: str) -> User:
        """Gets a user based on their username"""
        try:
            command_string: str = "SELECT * FROM Users WHERE Username = ?"
            self.cursor.execute(command_string, (username,))
            res = self.cursor.fetchone()
            if res is None: return None
            user: User = User(res[1], res[2], res[0])
            return user
        except sqlite3.DatabaseError:
            return None

    def get_user_by_id(self, user_id: int) -> User:
        """Gets a user based on their username"""
        print(user_id)
        command_string: str = "SELECT * FROM Users WHERE UserId = ?"
        self.cursor.execute(command_string, (user_id,))
        user_data = self.cursor.fetchone()

        print(user_data)
        if user_data:
            return User(
                userId=user_data[0], username=user_data[1], password=user_data[2]
            )
        return None

    # ------------------------------------------------------
    # User Recipe Interactions
    # ------------------------------------------------------

    def create_recipe(self, recipe: Recipe, user_id: int):
        """Creates a recipe based on the object provided"""
        try:
            print(recipe)
            command_string: str = """INSERT INTO Recipes (name, cookTime, prepTime, totalTime,
                                    description, category, rating, calories, fat, saturatedFat, cholesterol, sodium, carbs, fiber, sugar, protein, servings)   
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            self.cursor.execute(
                command_string,
                (
                    recipe.name,
                    recipe.cookTime,
                    recipe.prepTime,
                    recipe.totalTime,
                    recipe.description,
                    recipe.category,
                    recipe.rating,
                    recipe.calories,
                    recipe.fat,
                    recipe.saturatedFat,
                    recipe.cholesterol,
                    recipe.sodium,
                    recipe.carbs,
                    recipe.fiber,
                    recipe.sugar,
                    recipe.protein,
                    recipe.servings,
                ),
            )

            recipe_id: int = self.cursor.lastrowid

            for image in recipe.images:
                command_string: str = (
                    """INSERT INTO Images (recipeId, imageUrl) VALUES (?, ?)"""
                )
                self.cursor.execute(
                    command_string,
                    (
                        recipe_id,
                        image,
                    ),
                )

            for tag in recipe.tags:
                command_string: str = (
                    """INSERT INTO Tags (recipeId, tag) VALUES (?, ?)"""
                )
                self.cursor.execute(
                    command_string,
                    (
                        recipe_id,
                        tag,
                    ),
                )

            for ingredient in recipe.ingredients:
                command_string: str = (
                    """INSERT INTO Ingredients (recipeId, name, amount) VALUES (?, ?, ?)"""
                )
                self.cursor.execute(
                    command_string,
                    (
                        recipe_id,
                        ingredient,
                        0,
                    ),
                )

            for instructions in recipe.instructions:
                command_string: str = (
                    """INSERT INTO Instructions (recipeId, step, instruction) VALUES (?, ?, ?)"""
                )
                self.cursor.execute(
                    command_string,
                    (
                        recipe_id,
                        instructions.step,
                        instructions.instruction,
                    ),
                )

            command_string: str = (
                """INSERT INTO UserRecipes (recipeId, userId) VALUES (?, ?)"""
            )
            self.cursor.execute(
                command_string,
                (
                    recipe_id,
                    user_id,
                ),
            )

            self.conn.commit()
            return recipe_id

        except sqlite3.DatabaseError as e:
            print(e)
            return False

    def get_recipe(self, recipe_id: int):
        """Gets a recipe based on its id"""
        try:
            command_string: str = """SELECT * FROM Recipes WHERE recipeId = ?"""
            self.cursor.execute(command_string, (recipe_id,))
            recipe_res = self.cursor.fetchone()
            if not recipe_res:
                print("No recipe value found.")
                return None

            # print(recipeRes)

            command_string: str = """SELECT * FROM Images WHERE recipeId = ?"""
            self.cursor.execute(command_string, (recipe_id,))
            image_res = self.cursor.fetchall()
            image_list: list[str] = []
            for image in image_res:
                image_list.append(image[1])

            command_string: str = """SELECT * FROM Tags WHERE recipeId = ?"""
            self.cursor.execute(command_string, (recipe_id,))
            tags_res = self.cursor.fetchall()
            tags_list: list[str] = []
            for tag in tags_res:
                tags_list.append(tag[1])

            # print("got tags")
            command_string: str = """SELECT * FROM Ingredients WHERE recipeId = ?"""
            self.cursor.execute(command_string, (recipe_id,))
            ingredient_res = self.cursor.fetchall()
            ingredients_list: list[str] = []
            for _, ingredient, _ in ingredient_res:
                ingredients_list.append(ingredient)

            command_string: str = """SELECT * FROM Instructions WHERE recipeId = ?"""
            self.cursor.execute(command_string, (recipe_id,))
            instructions_res = self.cursor.fetchall()
            instructions_list: list[Instruction] = []
            for _, step, instruction in instructions_res:
                instructions_list.append(
                    Instruction(step=step, instruction=instruction)
                )

            # print(instructionsList)
            recipe: Recipe = Recipe(
                recipeId=recipe_res[0],
                name=recipe_res[1],
                cookTime=recipe_res[2],
                prepTime=recipe_res[3],
                totalTime=recipe_res[4],
                description=recipe_res[5],
                category=recipe_res[6],
                rating=recipe_res[7],
                calories=recipe_res[8],
                fat=recipe_res[9],
                saturatedFat=recipe_res[10],
                cholesterol=recipe_res[11],
                sodium=recipe_res[12],
                carbs=recipe_res[13],
                fiber=recipe_res[14],
                sugar=recipe_res[15],
                protein=recipe_res[16],
                servings=recipe_res[17],
                images=image_list,
                tags=tags_list,
                ingredients=ingredients_list,
                instructions=instructions_list,
            )

            return recipe

        except sqlite3.DatabaseError as e:
            print(e)
            return None

    def update_recipe(self, old_recipe_id: int, new_recipe: Recipe):
        """Updates a recipe to have the data of the new recipe"""
        recipe_owner: int = self.get_recipe_owner_by_recipe_id(old_recipe_id)
        self.delete_recipe(old_recipe_id)
        self.create_recipe(new_recipe, recipe_owner)

    def delete_recipe(self, recipe_id: int):
        """Deletes a recipe from the db"""
        try:
            command_string: str = """DELETE FROM Recipes WHERE recipeId = ?"""
            self.cursor.execute(command_string, (recipe_id,))
            return True

        except sqlite3.DatabaseError as e:
            print(e)
            return False

    def get_recipe_owner_by_recipe_id(self, recipe_id: int):
        """Gets the owner of the recipe"""
        try:
            command_string: str = (
                """SELECT userId FROM UserRecipes WHERE recipeId = ?"""
            )
            self.cursor.execute(command_string, (recipe_id,))
            res = self.cursor.fetchone()
            user_id = res[0]
            user: User = self.get_user_by_id(user_id)
            return user
        except sqlite3.DatabaseError as e:
            print(e)
            return None

    def get_recipes_owned_by_user_id(self, user_id: int):
        """Gets the owner of the recipe"""
        try:
            command_string: str = (
                """SELECT recipeId FROM UserRecipes WHERE userId = ?"""
            )
            self.cursor.execute(command_string, (user_id,))
            res = self.cursor.fetchall()
            return res

        except sqlite3.DatabaseError as e:
            print(e)
            return None

    # ------------------------------------------------------
    # Favorite Recipe Interactions
    # ------------------------------------------------------

    def unfavorite_recipe(self, user_id: int, recipe_id: int):
        """Unfavorites a recipe"""
        try:
            command_string: str = (
                """DELETE FROM UserFavorites WHERE recipeId = ? AND userId = ?"""
            )
            self.cursor.execute(
                command_string,
                (
                    recipe_id,
                    user_id,
                ),
            )
            return True

        except sqlite3.DatabaseError as e:
            print(e)
            return False

    def favorite_recipe(self, user_id: int, recipe_id: int):
        """Favorites a recipe"""
        try:
            command_string: str = (
                """INSERT INTO UserFavorites (recipeId, userId) VALUES (?, ?)"""
            )
            self.cursor.execute(
                command_string,
                (
                    recipe_id,
                    user_id,
                ),
            )
            return True

        except sqlite3.DatabaseError as e:
            print(e)
            return False

    def get_favorite_recipes(self, user_id: int):
        """Gets someones favorite recipes"""
        try:
            command_string: str = """SELECT * FROM UserFavorites WHERE userId = ?"""
            self.cursor.execute(command_string, (user_id,))
            res = self.cursor.fetchall()
            return res

        except sqlite3.DatabaseError as e:
            print(e)
            return None

    # ------------------------------------------------------
    # Recipe Search Interactions
    # ------------------------------------------------------

    def get_count_recipes_by_ingredients(
        self,
        ings: List[str],
    ):
        """Retrieves a count of recipe ids containing the given ingredients"""
        try:
            count_command: str = (
                """SELECT recipeId FROM (SELECT DISTINCT name, recipeId FROM ingredients WHERE name IN (%s)) GROUP BY recipeId HAVING COUNT(name) >= ? ;"""
                % ",".join("?" * len(ings))
            )
            res = self.cursor.execute(
                count_command,
                (
                    *ings,
                    len(ings),
                ),
            )
            count = len(res.fetchall())
            return count
        except sqlite3.DatabaseError as e:
            print(e)
            return -1

    def get_recipes_by_ingredient(self, ings: List[str], page: int, per_page: int = 10):
        """Retrieves a list of recipe ids containing the given ingredients limited by the number per page"""
        try:
            command_string: str = (
                """SELECT recipeId FROM (SELECT DISTINCT name, recipeId FROM ingredients WHERE name IN (%s)) GROUP BY recipeId HAVING COUNT(name) >= ? LIMIT ? OFFSET ?;"""
                % ",".join("?" * len(ings))
            )
            res = self.cursor.execute(
                command_string, (*ings, len(ings), per_page, page * per_page)
            )
            recipe_ids = (*res.fetchall(),)

            recipe_command: str = (
                """SELECT * FROM recipes WHERE recipeId IN (%s)"""
                % ",".join("?" * len(recipe_ids))
            )
            res = self.cursor.execute(
                recipe_command,
                tuple(id for recipeRecord in recipe_ids for id in recipeRecord),
            )

            recipe_objs = res.fetchall()

            recipes = []
            for recipe in recipe_objs:
                recipes.append(
                    RecipeListEntry(
                        name=recipe[1],
                        cookTime=recipe[2],
                        prepTime=recipe[3],
                        totalTime=recipe[4],
                        description=recipe[5],
                        category=recipe[6],
                        rating=recipe[7],
                        calories=recipe[8],
                        fat=recipe[9],
                        saturatedFat=recipe[10],
                        cholesterol=recipe[11],
                        sodium=recipe[12],
                        carbs=recipe[13],
                        fiber=recipe[14],
                        sugar=recipe[15],
                        protein=recipe[16],
                        servings=recipe[17],
                        recipeId=recipe[0],
                    )
                )

            print(recipes)
            return recipes
        except sqlite3.DatabaseError as e:
            print(e)
            return []

    def get_count_recipes_by_nutrition(
        self,
        calories_max: int,
        fat_max: int,
        sug_max: int,
        pro_max: int,
    ):
        """Retrieves a count of recipe ids containing the given ingredients"""
        try:
            count_command: str = (
                """SELECT * FROM recipes WHERE calories <= ? AND fat <= ? AND sugar <= ? and protein <= ? ;"""
            )
            res = self.cursor.execute(
                count_command,
                (
                    calories_max,
                    fat_max,
                    sug_max,
                    pro_max,
                ),
            )

            count = len(res.fetchall())
            return count
        except sqlite3.DatabaseError as e:
            print(e)
            return -1

    def get_recipes_by_nutrition(
        self,
        calories_max: int,
        fat_max: int,
        sug_max: int,
        pro_max: int,
        page: int,
        per_page: int = 10,
    ):
        """Retrieves a list of recipe ids containing the given ingredients limited by the number per page"""
        try:
            command_string: str = (
                """SELECT * FROM recipes WHERE calories <= ? AND fat <= ? AND sugar <= ? and protein <= ? LIMIT ? OFFSET ?; """
            )
            print(command_string)
            res = self.cursor.execute(
                command_string,
                (
                    calories_max,
                    fat_max,
                    sug_max,
                    pro_max,
                    per_page,
                    page * per_page,
                ),
            )

            recipe_objs = res.fetchall()

            recipes = []
            for recipe in recipe_objs:
                recipes.append(
                    RecipeListEntry(
                        name=recipe[1],
                        cookTime=recipe[2],
                        prepTime=recipe[3],
                        totalTime=recipe[4],
                        description=recipe[5],
                        category=recipe[6],
                        rating=recipe[7],
                        calories=recipe[8],
                        fat=recipe[9],
                        saturatedFat=recipe[10],
                        cholesterol=recipe[11],
                        sodium=recipe[12],
                        carbs=recipe[13],
                        fiber=recipe[14],
                        sugar=recipe[15],
                        protein=recipe[16],
                        servings=recipe[17],
                        recipeId=recipe[0],
                    )
                )

            return recipes
        except sqlite3.DatabaseError as e:
            print(e)
            return []

    def get_ingredient_list(self, ing: str):
        """Gets a list of ingredients based on the input"""
        try:
            command_string: str = (
                """SELECT name FROM ingredients WHERE name LIKE ? GROUP BY name LIMIT 10;"""
            )
            res = self.cursor.execute(command_string, (f"%{ing}%",))

            return res.fetchall()
        except sqlite3.DatabaseError as e:
            print(e)
            return []

    # ------------------------------------------------------
    # Meal Plan Interactions
    # ------------------------------------------------------

    def get_user_meal_plan(self, user_id: int):
        """Gets a user's meal plan"""
        try:
            command_string: str = "SELECT * FROM MealPlan WHERE userId = ?;"
            mealplan = self.cursor.execute(command_string, (user_id,)).fetchall()
            formatted_plan = [
                MealPlanEntry(day=mealitem[2], recipe={"recipeId": mealitem[1]})
                for mealitem in mealplan
            ]

            for entry in formatted_plan:
                entry.recipe.name = self.cursor.execute(
                    "SELECT name FROM recipes WHERE recipeId = ? ;",
                    (entry.recipe.recipeId,),
                ).fetchone()[0]

            return formatted_plan
        except sqlite3.DatabaseError as e:
            print(e)
            return []

    def update_user_meal_plan(self, user_id: int, day: int, recipe_id: int):
        """Updates a user's meal plan"""
        try:
            command_string: str = (
                "INSERT INTO MealPlan(userId,recipeId,dayOfWeek) VALUES (?,?,?) ON CONFLICT(userId, dayOfWeek) DO UPDATE SET recipeId = excluded.recipeId;"
            )
            self.cursor.execute(command_string, (user_id, recipe_id, day))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            print(e)
            return f"There was an error with updating the meal plan of user {user_id} for the day {day}"

    def remove_from_user_meal_plan(self, user_id: int, day: int):
        """Removes an item from the meal plan"""
        try:
            exists = self.cursor.execute(
                "SELECT * FROM MealPlan WHERE userId = ? AND dayOfWeek = ?;",
                (user_id, day),
            ).fetchone
            if exists is None:
                return f"An isntance with userId of {user_id} and day of {day} does not exist in the database."

            command_string: str = (
                "DELETE FROM MealPlan WHERE userId = ? AND dayOfWeek = ?"
            )
            self.cursor.execute(command_string, (user_id, day))
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            print(e)
            return f"There was an error removing the instance with userId of {user_id} and day of {day} from the database."

    # ------------------------------------------------------
    # Shopping List Interactions
    # ------------------------------------------------------

    def get_user_shopping_list(self, user_id: int):
        """Gets a user's shopping list"""
        try:
            command_string: str = "SELECT * FROM ShoppingList WHERE userId = ?;"
            shopping_list = self.cursor.execute(command_string, (user_id,)).fetchall()
            formatted_list = [
                ShoppingListItem(
                    name=shoppingItem[1],
                    quantity=shoppingItem[2],
                    unit=shoppingItem[3],
                    checked=shoppingItem[4],
                )
                for shoppingItem in shopping_list
            ]
            return formatted_list
        except sqlite3.DatabaseError as e:
            print(e)
            return []

    def update_shopping_list_item(
        self, user_id: int, name: str, quantity: int, unit: str, checked: bool
    ):
        """Updates a user's shopping list"""
        try:
            command_string: str = (
                "INSERT INTO ShoppingList(userId,name,quantity,unit,checked) VALUES (?,?,?,?,?) ON CONFLICT(userId, name) DO UPDATE SET quantity = excluded.quantity, unit = excluded.unit, checked = excluded.checked;"
            )
            self.cursor.execute(
                command_string,
                (
                    user_id,
                    name,
                    quantity,
                    unit,
                    1 if checked else 0,
                ),
            )
            self.conn.commit()

            return True
        except sqlite3.DatabaseError as e:
            print(e)
            return f"There was an error with updating the shopping list of user {user_id} for the item {name}"

    def remove_from_shopping_list(self, user_id: int, name: str):
        """Removes an item from the shopping list"""
        try:
            exists = self.cursor.execute(
                "SELECT * FROM ShoppingList WHERE userId = ? AND name = ?;",
                (user_id, name),
            ).fetchone()
            if exists is None:
                return f"An instance with userId of {user_id} and name of {name} does not exist in the database."

            command_string: str = (
                "DELETE FROM ShoppingList WHERE userId = ? AND name = ?;"
            )
            self.cursor.execute(command_string, (user_id, name))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            print(e)
            return f"There was an error removing the instance with userId of {user_id} and name of {name} from the database."

    # ------------------------------------------------------
    # Post Interactions
    # ------------------------------------------------------

    def add_post(self, post: Post) -> bool:
        """Adds a new post to the database"""
        try:
            command_string = "INSERT INTO Posts (UserId, Message, Image, RecipeId, Date) VALUES (?, ?, ?, ?, ?)"
            if post.recipe is not None:
                recipe_id = post.recipe.recipeId  # Already an int or None
            else:
                recipe_id = None
            self.cursor.execute(
                command_string,
                (
                    post.userId,
                    post.message,
                    post.image,
                    recipe_id,
                    post.date,
                ),
            )
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
            likes = self.get_post_reactions(post_id, "LIKE")
            dislikes = self.get_post_reactions(post_id, "DISLIKE")
            comments = self.get_post_comments(post_id)  # Fetch comments
            date_value = (
                post_data[5]
                if post_data[5] is not None
                else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            recipe_id = post_data[4]
            if recipe_id is not None:
                try:
                    recipe_id = int(recipe_id)
                    recipe_name = self.cursor.execute(
                        "SELECT name FROM recipes WHERE recipeId = ?;", (recipe_id,)
                    ).fetchone()[0]
                except (ValueError, TypeError, IndexError):
                    recipe_id = None
                    recipe_name = None

                recipe_obj = PostRecipe(recipeId=recipe_id, name=recipe_name)
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

    def get_all_posts(self) -> list[Post]:
        """Gets all posts from the database with their reactions and comments"""
        command_string = (
            "SELECT PostId, UserId, Message, Image, RecipeId, Date FROM Posts"
        )
        self.cursor.execute(command_string)
        posts_data = self.cursor.fetchall()
        posts = []
        for post_data in posts_data:
            likes = self.get_post_reactions(post_data[0], "LIKE")
            dislikes = self.get_post_reactions(post_data[0], "DISLIKE")
            comments = self.get_post_comments(post_data[0])  # Fetch comments
            date_value = (
                post_data[5]
                if post_data[5] is not None
                else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            recipe_id = post_data[4]
            recipe_obj = None  
            if recipe_id is not None:
                try:
                    recipe_id = int(recipe_id)
                    recipe_name = self.cursor.execute(
                        "SELECT name FROM recipes WHERE recipeId = ?;", (recipe_id,)
                    ).fetchone()[0]

                except (ValueError, TypeError):
                    recipe_id = None
                    recipe_name = ""

                recipe_obj = PostRecipe(recipeId=recipe_id, name=recipe_name)

                posts.append(
                    Post(
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
                )
        return posts

    def get_post_reactions(self, post_id: int, reaction_type: str) -> list[int]:
        """Gets all user IDs that have reacted to a post with a given reaction type"""
        command_string = (
            "SELECT UserId FROM PostReactions WHERE PostId = ? AND ReactionType = ?"
        )
        self.cursor.execute(command_string, (post_id, reaction_type))
        return [row[0] for row in self.cursor.fetchall()]

    def add_post_reaction(self, post_id: int, user_id: int, reaction_type: str) -> bool:
        """Adds a reaction to a post, updating if it already exists"""
        try:
            check_command = (
                "SELECT ReactionType FROM PostReactions WHERE PostId = ? AND UserId = ?"
            )
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
        """Removes a reaction from a post"""
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
            self.cursor.execute(
                "DELETE FROM PostReactions WHERE PostId = ?", (post_id,)
            )
            self.cursor.execute("DELETE FROM Comments WHERE PostId = ?", (post_id,))
            self.cursor.execute("DELETE FROM Posts WHERE PostId = ?", (post_id,))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            print(f"Error deleting post: {e}")
            return False

    def update_post(self, post_id: int, update_data: dict) -> bool:
        """Updates a post with the given data"""
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
            self.cursor.execute(
                command_string,
                (
                    comment.postId,
                    comment.userId,
                    comment.message,
                    comment.date or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
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
            return [
                Comment(
                    commentId=row[0],
                    userId=row[1],
                    postId=row[2],
                    message=row[3],
                    date=(
                        row[4]
                        if row[4] is not None
                        else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ),
                )
                for row in comments_data
            ]
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

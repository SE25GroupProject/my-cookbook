from api.db.convert_json_to_sql import insert_data
import sqlite3


def seedDatabase(databasePath, recipePath):

    conn = sqlite3.connect(databasePath)
    cursor = conn.cursor()
    ensureTables(cursor, conn)
    insert_data(databasePath, recipePath)

    conn.execute(
        """INSERT INTO Users (Username, Password) 
        VALUES ('TestUser', 'TestPass')""")
    conn.commit()


def ensureTables(cursor: sqlite3.Cursor, conn: sqlite3.Connection):
    """Ensures that the Users, Posts, and
    PostReactions tables exist in the database"""
    # Check and create Users table if it doesn't exist
    user_table = cursor.execute(
        """SELECT tbl_name FROM sqlite_master
        WHERE type='table' AND tbl_name='Users'""").fetchone()
    if user_table is None:
        with open("db/createUserTable.sql", "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            conn.commit()

    # Checking if the tables exist
    recipeTable = cursor.execute(
        """SELECT tbl_name FROM sqlite_master
        WHERE type='table' AND tbl_name='Recipes'""").fetchone()
    if recipeTable is None:
        with open("db/createRecipeTable.sql", "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            conn.commit()
    # Check and create Posts and PostReactions tables if they don't exist
    posts_table = cursor.execute(
        """SELECT tbl_name FROM sqlite_master
        WHERE type='table' AND tbl_name='Posts'""").fetchone()
    if posts_table is None:
        with open("db/createPostTable.sql", "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            conn.commit()

    # Checking if the Meal Plan table exist
    mealPlanTable = cursor.execute(
        """SELECT tbl_name FROM sqlite_master
        WHERE type='table' AND tbl_name='MealPlan'""").fetchone()
    shoppingTable = cursor.execute(
        """SELECT tbl_name FROM sqlite_master
        WHERE type='table' AND tbl_name='ShoppingList'""").fetchone()
    if mealPlanTable is None or shoppingTable is None:
        with open("db/createMealPrepTable.sql", "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            conn.commit()

    # Checking if the tables exist
    userRecipeTable = cursor.execute(
        """SELECT tbl_name FROM sqlite_master
        WHERE type='table' AND tbl_name='UserRecipes'""").fetchone()
    if userRecipeTable is None:
        with open("db/createUserRecipeTable.sql", "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            conn.commit()

    reactions_table = cursor.execute(
        """SELECT tbl_name FROM sqlite_master
        WHERE type='table' AND tbl_name='PostReactions'""").fetchone()
    if reactions_table is None:
        with open("db/createPostReactionsTable.sql", "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            conn.commit()

    # Check and create Comments table
    comments_table = cursor.execute(
        """SELECT tbl_name FROM sqlite_master
        WHERE type='table' AND tbl_name='Comments'""").fetchone()
    if comments_table is None:
        with open("db/createCommentsTable.sql", "r") as sql_file:
            cursor.executescript(sql_file.read())
            conn.commit()

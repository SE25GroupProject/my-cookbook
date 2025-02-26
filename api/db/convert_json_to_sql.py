"""File to convert the recipe.json file to a db file"""

import json
import sqlite3


def insert_data(path, recipes_json):
    """Inserts data into the db"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    with open("db/createRecipeTable.sql", "r", encoding="utf-8") as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)
        conn.commit()

    with open(recipes_json, "r", encoding="utf-8") as f:
        data = json.load(f)

        counter = 0
        for item in data:
            conn.execute(
                """
                INSERT INTO Recipes (name, cookTime,
                prepTime, totalTime, description, category,
                rating, calories, fat, saturatedFat,
                cholesterol, sodium, carbs, fiber,
                sugar, protein, servings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    item["name"],
                    item["cookTime"],
                    item["prepTime"],
                    item["totalTime"],
                    item["description"],
                    item["category"],
                    item["rating"],
                    item["rating"],
                    item["fat"],
                    item["saturatedFat"],
                    item["cholesterol"],
                    item["sodium"],
                    item["carbs"],
                    item["fiber"],
                    item["sugar"],
                    item["protein"],
                    item["servings"],
                ),
            )

            for image in item["images"]:
                conn.execute(
                    """
                    INSERT INTO Images (recipeId, imageUrl)
                    VALUES (?, ?)""",
                    (counter, image),
                )

            for tag in item["tags"]:
                conn.execute(
                    """
                    INSERT INTO Tags (recipeId, tag)
                    VALUES (?, ?)""",
                    (counter, tag),
                )

            ingredient_counter = 0
            for ingredient in item["ingredients"]:
                ingredient_to_use = None
                try:
                    ingQuant = item["ingredientQuantities"]
                    ingredient_to_use = ingQuant[ingredient_counter]
                except IndexError:
                    pass

                conn.execute(
                    """
                    INSERT INTO Ingredients (recipeId, name, amount)
                    VALUES (?, ?, ?)""",
                    (counter, ingredient, ingredient_to_use),
                )
                ingredient_counter += 1

            instruction_counter = 0
            for instruction in item["instructions"]:
                conn.execute(
                    """
                    INSERT INTO Instructions (recipeId, instruction, step)
                    VALUES (?, ?, ?)""",
                    (counter, instruction, instruction_counter),
                )
                instruction_counter += 1

            counter += 1
        conn.commit()

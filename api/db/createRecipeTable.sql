DROP TABLE IF EXISTS Recipes;

CREATE TABLE Recipes (
    recipeId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cookTime TEXT NOT NULL,
    prepTime TEXT NOT NULL,
    totalTime TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    rating REAL NOT NULL,
    calories REAL NOT NULL,
    fat REAL NOT NULL,
    saturatedFat REAL NOT NULL,
    cholesterol REAL NOT NULL,
    sodium REAL NOT NULL,
    carbs REAL NOT NULL,
    fiber REAL NOT NULL,
    sugar REAL NOT NULL,
    protein REAL NOT NULL,
    servings REAL NOT NULL
);

-- The table holding images for the recipes
DROP TABLE IF EXISTS Images;

CREATE TABLE Images (
    recipeId INTEGER NOT NULL,
    imageUrl TEXT NOT NULL,

    FOREIGN KEY (recipeId) REFERENCES Recipes(recipeId)
);

-- The table holding the tags for the recipes
DROP TABLE IF EXISTS Tags;

CREATE TABLE Tags (
    recipeId INTEGER NOT NULL,
    tag TEXT NOT NULL,
    
    FOREIGN KEY (recipeId) REFERENCES Recipes(recipeId)
);

-- The table holding the ingredients for the recipes
DROP TABLE IF EXISTS Ingredients;

CREATE TABLE Ingredients (
    recipeId INTEGER NOT NULL,
    name TEXT NOT NULL,
    amount REAL,

    FOREIGN KEY (recipeId) REFERENCES Recipes(recipeId)
);

-- The table holding the instructions
DROP TABLE IF EXISTS Instructions;

CREATE TABLE Instructions (
    recipeId INTEGER NOT NULL,
    step INTEGER NOT NULL,
    instruction TEXT NOT NULL,

    FOREIGN KEY (recipeId) REFERENCES Recipes(recipeId)
);
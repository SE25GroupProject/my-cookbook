-- If the Users table already exists we want to drop it to clean it up
DROP TABLE IF EXISTS MealPlan;
DROP TABLE IF EXISTS ShoppingList;

-- Creating the Users table
CREATE TABLE MealPlan (
    userId INTEGER NOT NULL,
    recipeId INTEGER NOT NULL,
    dayOfWeek INTEGER NOT NULL,

    UNIQUE(userId, dayOfWeek),
    CHECK (dayOfWeek >= 0 AND dayOfWeek <= 6)
    FOREIGN KEY (userId) REFERENCES Users(userId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (recipeId) REFERENCES Recipes(recipeId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE ShoppingList (
    userId INTEGER NOT NULL,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit TEXT NOT NULL,
    checked BOOLEAN NOT NULL,
    
    UNIQUE(userId, name), 
    CHECK (checked IN (0, 1)),
    CHECK (unit in ('kg','g','lb','oz','liter',
    'ml','dozen','bunch','head','loaf','piece','cup','tablespoon','teaspoon',
    'can','pack','box','jar','bottle','slice','packet')),

    FOREIGN KEY (userId) REFERENCES Users(userId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
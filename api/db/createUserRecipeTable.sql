
DROP TABLE IF EXISTS UserRecipes;

CREATE TABLE UserRecipes (
    recipeId INTEGER NOT NULL,
    userId INTEGER NOT NULL,
    FOREIGN KEY (recipeId) REFERENCES Recipes(recipeId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (userId) REFERENCES Users(recipeId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
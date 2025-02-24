-- If the Users table already exists we want to drop it to clean it up
DROP TABLE IF EXISTS Users;

-- Creating the Users table
CREATE TABLE Users (
    UserId INTEGER PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,

    UNIQUE(Username)
);

DROP TABLE IF EXISTS UserFavorites;

CREATE TABLE UserFavorites (
    UserId INTEGER NOT NULL,
    RecipeId INTEGER NOT NULL,
    FOREIGN KEY (recipeId) REFERENCES Recipes(recipeId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (userId) REFERENCES Users(recipeId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
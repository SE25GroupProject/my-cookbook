-- If the Users table already exists we want to drop it to clean it up
DROP TABLE IF EXISTS Users;

-- Creating the Users table
CREATE TABLE Users (
    UserId INTEGER PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,

    UNIQUE(Username)
);

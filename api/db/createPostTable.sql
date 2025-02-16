-- If the Posts table already exists, drop it to clean it up
DROP TABLE IF EXISTS Posts;

-- Creating the Posts table
CREATE TABLE Posts (
    PostId INTEGER PRIMARY KEY AUTOINCREMENT,  
    UserId INTEGER NOT NULL,                  
    Message TEXT NOT NULL,                   
    Image BLOB,                               
    RecipeId INTEGER,                     
    Date DATETIME DEFAULT CURRENT_TIMESTAMP,  
    Likes INTEGER DEFAULT 0,                  
    Dislikes INTEGER DEFAULT 0,               

    -- Foreign key constraint to link Posts to Users
    FOREIGN KEY (UserId) REFERENCES Users(UserId)
    FOREIGN KEY (RecipeId) REFERENCES Recipes(_id)
);

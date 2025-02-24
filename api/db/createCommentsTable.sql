-- Create a table to store user comments
CREATE TABLE Comments (
    CommentId INTEGER PRIMARY KEY AUTOINCREMENT,
    PostId INTEGER NOT NULL,
    UserId INTEGER NOT NULL,
    Message TEXT NOT NULL,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (PostId) REFERENCES Posts(PostId),
    FOREIGN KEY (UserId) REFERENCES Users(UserId)
);
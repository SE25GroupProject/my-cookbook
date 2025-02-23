-- Create a table to store user reactions (like or dislike)
CREATE TABLE PostReactions (
    PostId INTEGER NOT NULL,
    UserId INTEGER NOT NULL,
    ReactionType TEXT CHECK (ReactionType IN ('LIKE', 'DISLIKE')) NOT NULL,
    PRIMARY KEY (PostId, UserId), -- Ensures a user can only react to a post once
    FOREIGN KEY (PostId) REFERENCES Posts(PostId),
    FOREIGN KEY (UserId) REFERENCES Users(UserId)
);
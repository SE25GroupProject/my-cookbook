"""
Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com
"""

import sys
import os
import certifi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.db_middleware import DBConnectionMiddleware
from api.routes import router, userRouter, mealPlanRouter
from api.routes import shoppingRouter, postRouter

sys.path.insert(0, "../")

app = FastAPI()
app.include_router(router)

ca = certifi.where()

config = {
    "ATLAS_URI": os.getenv("ATLAS_URI"),
    "DB_NAME": os.getenv("DB_NAME"),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "PORT": os.getenv("PORT"),
}
app = FastAPI()

origins = ["http://localhost:3000", "*"]

app.add_middleware(DBConnectionMiddleware, db_path="db/cookbook.db")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_db_client():
    """Initializes the database client when the application starts"""
    # app.mongodb_client = MongoClient(config["ATLAS_URI"],
    #                                  tlsCAFile=ca)
    # app.database = app.mongodb_client[config["DB_NAME"]]


@app.on_event("shutdown")
def shutdown_db_client():
    """Closes the database client when the application shuts down"""
    # app.mongodb_client.close()


app.include_router(router, tags=["recipes"], prefix="/recipe")
app.include_router(userRouter, tags=["user"], prefix="/user")
app.include_router(mealPlanRouter, tags=["mealplan"], prefix="/meal-plan")
app.include_router(shoppingRouter, tags=["shopping"], prefix="/shopping-list")
app.include_router(postRouter, tags=["post"], prefix="/posts")


def get_database():
    """Returns the database connection."""
    # return app.database

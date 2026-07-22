# ==================================================
# Import Required Libraries
# ==================================================

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schema ,utils
from .database import engine, get_db
from .routers import post,user,auth


# ==================================================
# Create Database Tables
# ==================================================

models.Base.metadata.create_all(bind=engine)

# ==================================================
# Initialize FastAPI Application
# ==================================================

app = FastAPI()


# ==================================================
# Database Connection
# ==================================================

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="Aakash123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connected successfully")
        break

    except Exception as error:
        print("Error while connecting to database", error)
        time.sleep(2)  # Retry after 2 seconds


# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")  # Root endpoint
def read_root():
    return {"Hello": "World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

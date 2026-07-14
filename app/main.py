# ==================================================
# Import Required Libraries
# ==================================================

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# ==================================================
# Initialize FastAPI Application
# ==================================================

app = FastAPI()


# ==================================================
# Pydantic Model
# ==================================================

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# ==================================================
# Database Connection
# ==================================================

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="Aakash@123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connected successfully")
        break

    except Exception as error:
        print("Error while connecting to database", error)
        time.sleep(2)  # Retry after 2 sec




# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")  # Root endpoint
def read_root():
    return {"Hello": "World"}


# ==================================================
# Get All Posts
# ==================================================

@app.get("/post")  # Fetch all posts
def get_posts():
    cursor.execute("SELECT * FROM posts")
    post = cursor.fetchall()
    print(post)
    return {"data": post}

    # return {"message": "This is a GET request to the /post endpoint"}


# ==================================================
# Create New Post
# ==================================================

@app.post("/CreatePost")  # Create a post
def create_post(new_post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (new_post.title, new_post.content, new_post.published),
    )

    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

    # return {"New_post": f"Title : {new_post.title}, Content: {new_post.content}"}


# ==================================================
# Get Latest Post
# ==================================================

@app.get("/post/lastest")
def get_latest_post():
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    latest_post = cursor.fetchone()
    return {"data": latest_post}


# ==================================================
# Get Post By ID
# ==================================================

@app.get("/post/{ID}")
def get_post(ID: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s returning *", (str(ID),))
    post = cursor.fetchone()
    if post:
        return {"data": post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {ID} not found",
        )
    

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": "Post not found"}


# ==================================================
# Delete Post
# ==================================================

@app.delete("/post/{ID}")
def delete_post(ID: int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *",(str(ID)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post:
        return {"message": f"Post with ID {ID} has been deleted"}
    else:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {ID} not found",
    )


# ==================================================
# Update Post
# ==================================================

@app.put("/post/{ID}")
def update_post(ID: int, updated_post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *",
                   (updated_post.title, updated_post.content, updated_post.published, str(ID)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post:
        return {"data": updated_post}
    else:

        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f"Post with ID {ID} not found",
    )
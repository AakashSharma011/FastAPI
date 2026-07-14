                       #Importing the required libraries

from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

                        #Initializing the FastAPI app

app = FastAPI()                                         

                        #Defining a Pydantic model for the Post data structure

class Post(BaseModel):                                
    title: str
    content: str
    published: bool = True

                        # Connecting to the PostgreSQL database with retry logic


while True: 
    try:
        conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Aakash@123', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Error while connecting to database", error)
        time.sleep(2)                    # Wait for 2 seconds before retrying
    

My_posts=[{"title": "My first post", "content": "This is my first post", "ID": 1},
                   {"title": "My second post", "content": "This is my second post", "ID": 2}]
 
@app.get("/")                                           #/ is the root endpoint of the API
def read_root():
    return {"Hello": "World"}

@app.get("/post")                                        #/post is the endpoint of the API
def get_posts():
    cursor.execute("SELECT * FROM posts")
    post=cursor.fetchall()
    print(post)
    return {"data": post}
    #return {"message": "This is a GET request to the /post endpoint"}

@app.post("/CreatePost")                                 #/CreatePost is the endpoint of the API
def create_post(new_post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                   (new_post.title, new_post.content, new_post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post }
                           #Returning the created post

    #return {"New_post": f"Title : {new_post.title}, Content: {new_post.content}"}

                            #Retrives last post from the list of posts

@app.get("/post/lastest")
def get_latest_post():
    return {"data": My_posts[-1]}

                            # Retrieve a specific post by ID

@app.get("/post/{ID}")
def get_post(ID:int,response: Response):
    for post in My_posts:
        if post["ID"] == ID:
            return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {ID} not found")
    #response.status_code = status.HTTP_404_NOT_FOUND
    #return {"message": "Post not found"}


                            #Delete a specific post by ID

@app.delete("/post/{ID}")
def delete_post(ID:int):
    for index, post in enumerate(My_posts):
        if post["ID"] == ID:
            My_posts.pop(index)
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with ID {ID} has been deleted")
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {ID} not found")


                            #Update a specific post by ID

@app.put("/post/{ID}")
def update_post(ID:int, updated_post: Post):
    for index, post in enumerate(My_posts):
        if post["ID"] == ID:
            My_posts[index] = updated_post.dict()
            My_posts[index]["ID"] = ID  # Ensure the ID remains the same
            raise HTTPException(status_code=status.HTTP_200_OK, detail=f"Post with ID {ID} has been updated")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {ID} not found")


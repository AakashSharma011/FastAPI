#Importing the required libraries
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI() #Initializing the FastAPI app

class Post(BaseModel): #Defining a Pydantic model for the Post data structure
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

My_posts=[{"title": "My first post", "content": "This is my first post", "ID": 1},
                   {"title": "My second post", "content": "This is my second post", "ID": 2}]
 
@app.get("/")  #/ is the root endpoint of the API
def read_root():
    return {"Hello": "World"}

@app.get("/post")  #/post is the endpoint of the API
def get_post():
    return {"data": My_posts}
    #return {"message": "This is a GET request to the /post endpoint"}

@app.post("/CreatePost")                                 #/CreatePost is the endpoint of the API
def create_post(new_post: Post):
    post_dict=new_post.dict()                            #Converting the Pydantic model to a dictionary
    post_dict["ID"]=randrange(0,1000000)                 #Generating a random ID for the new post
    My_posts.append(post_dict)                           #Appending the new post to the list of posts
    return {"data": post_dict}                           #Returning the created post

    #return {"New_post": f"Title : {new_post.title}, Content: {new_post.content}"}
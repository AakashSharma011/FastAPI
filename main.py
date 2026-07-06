#Importing the required libraries
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI() #Initializing the FastAPI app

class Post(BaseModel): #Defining a Pydantic model for the Post data structure
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
 
@app.get("/")  #/ is the root endpoint of the API
def read_root():
    return {"Hello": "World"}

@app.get("/post")  #/post is the endpoint of the API
def get_post():
    return {"message": "This is a GET request to the /post endpoint"}

@app.post("/CreatePost")  #/CreatePost is the endpoint of the API
def create_post(new_post: Post):
    print(new_post.rating)
    return {"New_post": f"Title : {new_post.title}, Content: {new_post.content}"}
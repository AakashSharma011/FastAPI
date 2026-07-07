#Importing the required libraries
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()                                         #Initializing the FastAPI app

class Post(BaseModel):                                  #Defining a Pydantic model for the Post data structure
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

My_posts=[{"title": "My first post", "content": "This is my first post", "ID": 1},
                   {"title": "My second post", "content": "This is my second post", "ID": 2}]
 
@app.get("/")                                           #/ is the root endpoint of the API
def read_root():
    return {"Hello": "World"}

@app.get("/post")                                        #/post is the endpoint of the API
def get_posts():
    return {"data": My_posts}
    #return {"message": "This is a GET request to the /post endpoint"}

@app.post("/CreatePost")                                 #/CreatePost is the endpoint of the API
def create_post(new_post: Post):
    post_dict=new_post.dict()                            #Converting the Pydantic model to a dictionary
    post_dict["ID"]=randrange(0,1000000)                 #Generating a random ID for the new post
    My_posts.append(post_dict)  
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail="Post Successfully created")  #Raising an HTTPException with a 201 status code and a message
    #return {"data": post_dict}                           #Returning the created post

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

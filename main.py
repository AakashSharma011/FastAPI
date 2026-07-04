from fastapi import FastAPI
app = FastAPI()
 
@app.get("/")  #/ is the root endpoint of the API
def read_root():
    return {"Hello": "World"}

@app.get("/post")  #/post is the endpoint of the API
def get_post():
    return {"message": "This is a GET request to the /post endpoint"}

@app.post("/CreatePost")  #/CreatePost is the endpoint of the API
def create_post():
    return {"message": "This is a POST request to the /CreatePost endpoint"}
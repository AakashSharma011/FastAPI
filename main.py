from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()
 
@app.get("/")  #/ is the root endpoint of the API
def read_root():
    return {"Hello": "World"}

@app.get("/post")  #/post is the endpoint of the API
def get_post():
    return {"message": "This is a GET request to the /post endpoint"}

@app.post("/CreatePost")  #/CreatePost is the endpoint of the API
def create_post(payLoad: dict = Body(...)):
    print(payLoad)
    return {"New_post":f"Title : {payLoad['title']}, Content: {payLoad['content']}"}
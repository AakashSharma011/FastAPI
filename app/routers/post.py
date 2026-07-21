from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from .. import models, schema ,utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router=APIRouter()


# ==================================================
# Get All Posts
# ==================================================

@router.get("/post")  # Fetch all posts
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

    # return {"message": "This is a GET request to the /post endpoint"}


# ==================================================
# Create New Post
# ==================================================

@router.post("/CreatePost", response_model=schema.Post)  # Create a new post
def create_post(Post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (new_post.title, new_post.content, new_post.published),
    # )

    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**Post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

    # return {"New_post": f"Title : {new_post.title}, Content: {new_post.content}"}



# ==================================================
# Get Post By ID
# ==================================================

@router.get("/post/{ID}",response_model=schema.Post   )  # Fetch a post by its ID
def get_post(ID: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s returning *", (str(ID),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == ID).first()

    if post:
        return  post
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

@router.delete("/post/{ID}")  # Delete a post by its ID
def delete_post(ID: int, db: Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == ID).first()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {ID} not found"
        )

    db.delete(deleted_post)
    db.commit()

    return {"message": f"Post with ID {ID} has been deleted"}


# ==================================================
# Update Post
# ==================================================

@router.put("/post/{ID}",response_model=schema.Post)  # Update an existing post by its ID
def update_post(ID: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *",
    #     (updated_post.title, updated_post.content, updated_post.published, str(ID))
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == ID).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {ID} not found"
        )

    for key, value in updated_post.dict().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)

    return  post
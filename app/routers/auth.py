from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schema, utils , oauth

router = APIRouter(tags=['Authentication'])

@router.post("/login",response_model=schema.Token)
def login(User_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user= db.query(models.User).filter(models.User.email == User_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(User_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #create a token and return it  
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return{"access_token": access_token,"token_type": "bearer"}
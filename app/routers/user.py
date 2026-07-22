
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from .. import models, schema ,utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/usesr",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def Create_user(user:schema.User,db:Session=Depends(get_db)):

    user.password=utils.hash(user.password)   
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{ID}",response_model=schema.UserOut)
def get_user(ID:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==ID).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with ID {ID} not found")
    return user
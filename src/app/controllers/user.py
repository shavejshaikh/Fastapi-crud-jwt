from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from app.data.database import get_db
from app.data import schemas, models
from app.controllers.auth import PasswordHashing
from app.controllers.auth import jwt_auth_wrapper
from fastapi import APIRouter, HTTPException, status, Depends


router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model = List[schemas.UserOut], summary="Get the list of all users")
async def get_users(db: Session = Depends(get_db), payload=Depends(jwt_auth_wrapper)):
    try:
        users = db.query(models.User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    


@router.post("/", status_code =status.HTTP_201_CREATED, summary="Create the user")
async def create_user(request: schemas.User, db: Session = Depends(get_db), payload=Depends(jwt_auth_wrapper)):
    try:
        check_user_email = db.query(models.User).filter(models.User.email == request.email).first() is not None
        if check_user_email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email is already exist")
        
        password_hashing = PasswordHashing()
        hashed_password = password_hashing.hash_password(password=request.password)
        new_user = models.User(name = request.name, email = request.email, password = hashed_password, added_on = datetime.now())
        db.add(new_user)
        db.commit()
        return "Successfully created a user"
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    
@router.put("/{user_id}/", status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id:int, request:schemas.UserUpdate, db:Session = Depends(get_db), payload=Depends(jwt_auth_wrapper)):
    user = db.query(models.User).filter(models.User.id == user_id)
    if user.first():
        user_update_dict = request.dict(exclude_none=True)
        user_update_dict['update_on'] = datetime.now()
        user.update(user_update_dict)
        db.commit()
        return "successfully updated the user data"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user information for user_id {user_id}")

@router.get("/{user_id}/", status_code=status.HTTP_200_OK, response_model = schemas.UserOut)
async def get_user(user_id: int, db: Session = Depends(get_db), payload=Depends(jwt_auth_wrapper)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Not found user information for user_id {user_id}")
    

@router.delete("/{user_id}/", status_code =status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int, db: Session = Depends(get_db), payload=Depends(jwt_auth_wrapper)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return "Successfully deleted user"
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Not found user information for user_id {user_id}")
    
@router.delete("/", status_code=status.HTTP_202_ACCEPTED)
async def delete_all_user(db: Session = Depends(get_db), payload=Depends(jwt_auth_wrapper)):
    try:
        db.query(models.User).delete()
        db.commit()
        return "Successfully flush all the user data"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete the user data")
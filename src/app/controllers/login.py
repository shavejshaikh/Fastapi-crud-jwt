from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from app.data.database import get_db
from app.data import schemas
from app.controllers.auth import generate_jwt_access_token, authenticate_user
from app.controllers.auth import decode_auth_token

router = APIRouter()


@router.post("/token", status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def login(request: schemas.Login, db:Session= Depends(get_db)):
    user = authenticate_user(db, username = request.email, password= request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    access_token = generate_jwt_access_token(name=user.name, email=user.email)
    return {"access_token":access_token, "token_type":"bearer"}

    

@router.post("/users/me/", response_model=schemas.UserOut)
async def read_users_token(request: schemas.Token,db:Session=Depends(get_db)):
    user_info = decode_auth_token(request.access_token)
    return user_info
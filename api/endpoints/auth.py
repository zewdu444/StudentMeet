from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter
from passlib.context import CryptContext
import uuid
import schemas.user as User_Schemas
import models.user as User_Models
from sqlalchemy.orm import Session
from database import get_db, engine

router =APIRouter(prefix="/auth", tags=["Authentication"], responses={404: {"description": "Not found"}})
User_Models.Base.metadata.create_all(bind=engine)

user_token_info = {
    "access_token": "string",
    "token_type": "bearer",
    "user_id": "string"
}
# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# authenticate user

def authenticate_user(db: Session, university_id: int, password: str):
    user = db.query(User_Models.Users).filter(User_Models.Users.university_id == university_id).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(user_token_info,token)
    if(token != user_token_info["access_token"]) :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = db.query(User_Models.Users).filter(User_Models.Users.university_id == user_token_info["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user

# login user
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    user_token_info["access_token"] = str(uuid.uuid4())
    user_token_info["user_id"] = user.university_id
    return user_token_info
    return {"message": "User logged in successfully"}

# create new user

@router.post("/register")
async def user_registration(user:User_Schemas.UserCreate, db:Session =Depends(get_db)):
    find_user = db.query(User_Models.Users).filter(User_Models.Users.email == user.email).first()
    if find_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    new_user = User_Models.Users(**user.dict())
    new_user.hashed_password = get_password_hash(user.hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

def get_user_exception():
   return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

def get_login_exception():
   return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

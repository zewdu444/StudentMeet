from fastapi import APIRouter, Depends, HTTPException, status
import schemas.user as User_Schemas
import models.user as User_Models
from database import get_db, engine
from sqlalchemy.orm import Session, Query
from sqlalchemy import or_
from typing import Optional
from .auth import get_current_user, get_user_exception
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
router = APIRouter(prefix="/users", tags=["Users"], responses={404: {"description": "Not found"}})
User_Models.Base.metadata.create_all(bind=engine)

# get all users
@router.get("/", response_model =list[User_Schemas.User])
async def get_users(db: Session = Depends(get_db),
                           login_user:dict=Depends(get_current_user),
                           search: Optional[str] = None,
                           role: Optional[str] = None,
                           sort_by: Optional[str] = None,
                           page_number: Optional[int] = 1,
                           page_size: Optional[int] = 10):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(User_Models.Users)
    # search by field
    if search:
        search_term = f"%{search}%"
        search_fields = [
           {
            'or': [
                {'field': 'firstname', 'op': 'ilike', 'value': search_term},
                {'field':'lastname', 'op': 'ilike', 'value': search_term},
                {'field':'email','op':'ilike', 'value':search_term},
            ],
           }
        ]
        query = apply_filters(query, search_fields, search_term)
    # filter by field
    if role:
        role_filter = [{'field':'role', 'op': '==', 'value': role}, ]
        query = apply_filters(query, role_filter, role)
    # order by
    if sort_by:
        sorted_by_fields = [{'field': sort_by, 'direction': 'asc'}]
        query = apply_sort(query, sorted_by_fields)
    # pagination
    query, pagination = apply_pagination(query, page_number=page_number, page_size=page_size)
    if len(query.all()) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return query.all()

# get user by id
@router.get("/{university_id}", response_model=User_Schemas.User)
async def get_user(university_id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    user = db.query(User_Models.Users).filter(User_Models.Users.university_id == university_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# delete user by id
@router.delete("/{university_id}")
async def delete_user(university_id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    user = db.query(User_Models.Users).filter(User_Models.Users.university_id == university_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# update user by id
@router.put("/{university_id}")
async def update_user(university_id: int, user: User_Schemas.UserUpdate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    user_update = db.query(User_Models.Users).filter(User_Models.Users.university_id == university_id).first()
    if not user_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(user_update, key, value)
    db.commit()
    return {"message": "User updated successfully"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, Query
from sqlalchemy import or_
from typing import Optional
from database import get_db, engine
import models.session as Session_Models
import models.user as User_Models
import schemas.session as Session_Schemas
import models.session_booking as Session_Bookings_Models
import schemas.session_booking as Session_Bookings_Schemas
from .auth import get_current_user, get_user_exception
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
from utils.slots import check_selected_slot
router = APIRouter(prefix="/sessions", tags=["Sessions"], responses={404: {"description": "Not found"}})


# get all sessions
@router.get("/", response_model =list[Session_Schemas.Session])
async def get_sessions(db: Session = Depends(get_db),
                          login_user:dict=Depends(get_current_user),
                          search: Optional[str] = None,
                          sort_by: Optional[str] = None,
                          page_number: Optional[int] = 1,
                          page_size: Optional[int] = 10):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(Session_Models.Sessions)
    # search by field
    if search:
        search_term = f"%{search}%"
        search_fields = [
           {
            'or': [
                {'field': 'session_description', 'op': 'ilike', 'value': search_term},
            ],
           }
        ]
        query = apply_filters(query, search_fields, search_term)
    # order by
    if sort_by:
        sorted_by_fields = [{'field': sort_by, 'direction': 'asc'}]
        query = apply_sort(query, sorted_by_fields)
    # pagination
    query, pagination = apply_pagination(query, page_number=page_number, page_size=page_size)
    if len(query.all()) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sessions found")
    sessions = query.all()
    for session in sessions:
        session.created_by_teacher = db.query(User_Models.Users).filter(User_Models.Users.university_id == session.created_by_teacher).first()
    return sessions

# get session by id
@router.get("/{session_id}", response_model=Session_Schemas.Session)
async def get_session(session_id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    session = db.query(Session_Models.Sessions).filter(Session_Models.Sessions.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    session.created_by_teacher = db.query(User_Models.Users).filter(User_Models.Users.university_id == session.created_by_teacher).first()
    return session

# create new session
@router.post("/")
async def create_session(session: Session_Schemas.SessionCreate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    # if login_user["role"] != "teacher":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only teachers can create sessions")
    # if not check_selected_slot(session.start_date, session.end_date):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid slot selected")
    new_session = Session_Models.Sessions(**session.dict())
    new_session.created_by_teacher = login_user["university_id"]
    db.add(new_session)
    db.commit()
    return  {"message": "Session created successfully"}

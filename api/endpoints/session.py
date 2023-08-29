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
                          session_status : Optional[str] = None,
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
    # filter by status
    if session_status:
        session_status_criteria = [[{'field': 'status', 'op': '==', 'value': session_status}]]
        query = apply_filters(query, session_status_criteria, session_status)
        print(query.all())
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
    print(login_user.role)
    if login_user is None:
        raise get_user_exception
    if login_user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only teachers can create sessions")
    if not check_selected_slot(session.session_start, session.session_end):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid slot selected")
    new_session = Session_Models.Sessions(**session.dict())
    new_session.created_by_teacher = login_user.university_id
    db.add(new_session)
    db.commit()
    return  {"message": "Session created successfully"}
# booked session
@router.post("/book/{session_id}")
async def booked_session(session_id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    if login_user.role != "student":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only students can book sessions")
    session = db.query(Session_Models.Sessions).filter(Session_Models.Sessions.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    if session.status != "created":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session not available for booking")
    if not check_selected_slot(session.session_start, session.session_end):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid slot selected")
    new_session_booking = Session_Bookings_Models.Session_bookings(session_id=session_id, booked_by_student=login_user.university_id)
    session.status = "pending"
    db.add(new_session_booking)
    db.commit()
    return  {"message": "Session booked successfully"}

# delete booked session
@router.delete("/book/{session_id}")
async def delete_booked_session(session_id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    session_booking = db.query(Session_Bookings_Models.Session_bookings).filter(Session_Bookings_Models.Session_bookings.session_id == session_id).first()
    if not session_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session booking not found")
    session = db.query(Session_Models.Sessions).filter(Session_Models.Sessions.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    session.status = "created"
    db.delete(session_booking)
    db.commit()
    return  {"message": "Session booking deleted successfully"}

# update session
@router.put("/{session_id}")
async def update_session(session_id: int, session: Session_Schemas.SessionUpdate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    if login_user.role != "teacher":
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only teachers can update sessions")
    if session.session_start is not None and session.session_end is not None:
        if not check_selected_slot(session.session_start, session.session_end):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid slot selected")
    update_session = db.query(Session_Models.Sessions).filter(Session_Models.Sessions.session_id == session_id).first()
    if not update_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    for key, value in session.dict(exclude_unset=True).items():
        setattr(update_session, key, value)
    db.commit()
    return {"message": "Session updated succefully"}

# list all booked sessions by teacher id
@router.get("/booked/{teacher_id}",response_model=list[Session_Bookings_Schemas.Session_bookings])
async  def get_booked(teacher_id:int,db: Session = Depends(get_db),login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    if login_user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only teachers can view booked sessions")
    query :Query = db.query(Session_Bookings_Models.Session_bookings).join(Session_Models.Sessions, Session_Bookings_Models.Session_bookings.session_id == Session_Models.Sessions.session_id).filter(Session_Models.Sessions.created_by_teacher == teacher_id).filter(Session_Models.Sessions.status== "pending")
    if len(query.all()) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sessions found")
    sessions = query.all()
    for session in sessions:
        session.booked_by_student = db.query(User_Models.Users).filter(User_Models.Users.university_id == session.booked_by_student).first()
        session.session_id = db.query(Session_Models.Sessions).filter(Session_Models.Sessions.session_id == session.session_id).first()
    for session in sessions:
         session.session_id.created_by_teacher = db.query(User_Models.Users).filter(User_Models.Users.university_id == session.session_id.created_by_teacher).first()
    return sessions

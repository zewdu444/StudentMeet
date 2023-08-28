from fastapi import APIRouter
from endpoints import auth, user, session
api_router =APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(session.router)

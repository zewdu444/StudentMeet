from sqlalchemy.orm import Session, Query
from sqlalchemy import or_
from typing import Optional
from .auth import get_current_user, get_user_exception
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination

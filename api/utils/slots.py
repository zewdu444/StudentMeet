from datetime import datetime, timedelta
from fastapi import HTTPException , status
def check_selected_slot(start_date, end_date):
     if start_date > end_date:
           raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot be greater than end date")
     if start_date.weekday() !=3  and  start_date.weekday()!=4:
           raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="Start date  is not a Thursday or Friday")
     if end_date.weekday() !=3  and  end_date.weekday()!=4:
             raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="End date  is not a Thursday or Friday")
     if start_date.hour !=10 or start_date.minute !=0:
           raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="Start time is not 10:00 AM")
     if end_date.hour !=11 or end_date.minute !=0:
             raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="End time is not 11:00 AM")
     return True

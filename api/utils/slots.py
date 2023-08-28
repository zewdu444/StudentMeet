from datetime import datetime, timedelta

def check_selected_slot(start_date, end_date):
     if start_date > end_date:
           raise ValueError("Start date cannot be greater than end date")
     if start_date.weekday() !=3  or end_date.weekday() !=3 or start_date.weekday() !=4 or end_date.weekday() !=4:
           raise ValueError("Selected date is not a Thursday or Friday")
     if start_date.hour !=10 or start_date.minute !=0:
           raise ValueError("Selected time is not 10:00 AM")
     if end_date.hour !=11 or end_date.minute !=0:
           raise ValueError("Selected time is not 11:00 AM")
     return True

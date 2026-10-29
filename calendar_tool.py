from datetime import datetime,timedelta
import calendar
import holidays
from langchain_core.tools import tool
india_holidays=holidays.India()
def is_second_or_fourth_saturday(date):
    """
    Return True if Date is 2nd or 4th saturday of the month
    """
    if date.weekday()!=5:
        return False
    month_calendar=calendar.monthcalendar(date.year,date.month)
    saturday_number=0
    for week in month_calendar:
        if week[calendar.SATURDAY]!=0:
            saturday_number+=1
            if week[calendar.SATURDAY]==date.day:
                return saturday_number in (2,4)
    return False

@tool
def calendar_tool(start_date,end_date):
    """
    Calculate work leave days between 2 dates

    Excludes:
    - Sundays
    - 2nd Saturdays
    - 4th Saturdays
    - Indian Public Holidays
    Date format: YYYY-MM-DD
    """
    start=datetime.strptime(start_date,"%Y-%m-%d").date()
    end=datetime.strptime(end_date,"%Y-%m-%d").date()
    current=start
    leave_days=0
    weekends=[]
    holiday_list=[]
    counted_days=[]
    while current<=end:
        if current.weekday()==6:
            weekends.append(str(current))
        elif is_second_or_fourth_saturday(current):
            weekends.append(str(current))
        elif current in india_holidays:
            holiday_list.append(
                {
                    "date":str(current),
                    "name":india_holidays[current]

                }
            )
        else:
            leave_days+=1
            counted_days.append(str(current))
        current+=timedelta(days=1)
    return {
         "calendar_days": (end - start).days + 1,
         "leave_days": leave_days,
         "working_days": counted_days,
         "weekends": weekends,
         "holidays": holiday_list
    }
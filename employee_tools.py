import os
import mysql.connector
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


# =====================================================
# DATABASE CONNECTION
# =====================================================

from db import get_connection


# =====================================================
# EMPLOYEE DETAILS
# =====================================================

@tool
def employee_details_tool(employee_id: int):
    """
    Retrieve an employee's personal information.

    Intended for employee self-service.
    (In a production application, employee_id would come from
    the authenticated user rather than being supplied manually.)
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        employee_id,
        name,
        department,
        role,
        manager,
        joining_date
    FROM employees
    WHERE employee_id = %s
    """

    cursor.execute(query, (employee_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return {"error": "Employee not found."}

    result["joining_date"] = str(result["joining_date"])

    return result


# =====================================================
# LEAVE BALANCE
# =====================================================

@tool
def leave_balance_tool(employee_id: int):
    """
    Retrieve an employee's leave balances.

    Intended for employee self-service.
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        employee_id,
        earned_leave,
        sick_leave,
        casual_leave
    FROM leave_balance
    WHERE employee_id = %s
    """

    cursor.execute(query, (employee_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return {"error": "Employee not found."}

    return result
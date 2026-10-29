import os
import mysql.connector
from dotenv import load_dotenv
from langchain_core.tools import tool
from services.employee_services import (get_employee_details,get_leave_balance,)
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
    Retrieve complete details of any employee.
    """
    return get_employee_details(employee_id)



# =====================================================
# LEAVE BALANCE
# =====================================================

@tool
def leave_balance_tool(employee_id: int):
    """
    Retrieve leave balance of any employee.
    """
    return get_leave_balance(employee_id)


# =====================================================
# LIST ALL EMPLOYEES
# =====================================================

@tool
def employee_list_tool():
    """
    List all employees.
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        *
    FROM employees
    ORDER BY employee_id
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in results:
        row["joining_date"] = str(row["joining_date"])

    return results


# =====================================================
# SEARCH EMPLOYEE
# =====================================================

@tool
def employee_search_tool(search: str):
    """
    Search employee by ID or name.
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search.isdigit():

        query = """
        SELECT *
        FROM employees
        WHERE employee_id=%s
        """

        cursor.execute(query, (int(search),))

    else:

        query = """
        SELECT *
        FROM employees
        WHERE name LIKE %s
        """

        cursor.execute(query, (f"%{search}%",))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in results:
        row["joining_date"] = str(row["joining_date"])

    if not results:
        return {"error": "Employee not found."}

    return results


# =====================================================
# SEARCH BY DEPARTMENT
# =====================================================

@tool
def department_employees_tool(department: str):
    """
    Retrieve employees belonging to a department.
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        employee_id,
        name,
        role,
        joining_date
    FROM employees
    WHERE department=%s
    ORDER BY name
    """

    cursor.execute(query, (department,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in results:
        row["joining_date"] = str(row["joining_date"])

    return results


# =====================================================
# SEARCH BY ROLE
# =====================================================

@tool
def role_search_tool(role: str):
    """
    Retrieve employees having a specific role.
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        employee_id,
        name,
        department,
        joining_date
    FROM employees
    WHERE role=%s
    ORDER BY name
    """

    cursor.execute(query, (role,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in results:
        row["joining_date"] = str(row["joining_date"])

    return results


# =====================================================
# TOTAL EMPLOYEE COUNT
# =====================================================

@tool
def employee_count_tool():
    """
    Return total number of employees.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_employees": count
    }


# =====================================================
# EMPLOYEES UNDER A MANAGER
# =====================================================

@tool
def manager_tool(manager_name: str):
    """
    Retrieve employees reporting to a manager.
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        employee_id,
        name,
        department,
        role
    FROM employees
    WHERE manager LIKE %s
    ORDER BY name
    """

    cursor.execute(query, (f"%{manager_name}%",))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


# =====================================================
# JOINING DATE SEARCH
# =====================================================

@tool
def joining_date_tool(start_date: str, end_date: str):
    """
    Retrieve employees who joined between two dates.

    Date format:
    YYYY-MM-DD
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        employee_id,
        name,
        department,
        role,
        joining_date
    FROM employees
    WHERE joining_date BETWEEN %s AND %s
    ORDER BY joining_date
    """

    cursor.execute(query, (start_date, end_date))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in results:
        row["joining_date"] = str(row["joining_date"])

    return results
import os
import mysql.connector
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


# =====================================================
# DATABASE CONNECTION
# =====================================================
import os

print("HOST =", os.getenv("MYSQL_HOST"))
print("USER =", os.getenv("MYSQL_USER"))
print("DATABASE =", os.getenv("MYSQL_DATABASE"))

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

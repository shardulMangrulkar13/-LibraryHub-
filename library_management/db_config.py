import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123456",   # Enter your MySQL password here
        database="library_db"
    )

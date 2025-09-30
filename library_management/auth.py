import mysql.connector
from db_config import get_db_connection

def register_user(username, password, role='user'):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

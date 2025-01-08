import sqlite3
import hashlib
# פונקציה להדפסת כל המשתמשים במסד הנתונים
def print_users():
    with sqlite3.connect('GymTrucker.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users')  # מבצע שאילתא על כל המשתמשים
        users = c.fetchall()  # מקבל את כל השורות
        if users:
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}")
        else:
            print("No users found.")
print_users()
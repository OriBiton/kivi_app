import sqlite3
import hashlib
import re

# יצירת מסד נתונים אם לא קיים
def create_db():
    with sqlite3.connect('GymTrucker.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL
            )
        ''')
        conn.commit()


# הוספת משתמש חדש למסד הנתונים
def add_user(username, password, first_name):
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # הצפנת סיסמה
        with sqlite3.connect('GymTrucker.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password, first_name) VALUES (?, ?, ?)', 
                      (username, hashed_password, first_name))
            conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Username already exists. Please choose a different one.")


# עדכון מבנה מסד הנתונים להוספת עמודת first_name
def update_db():
    with sqlite3.connect('GymTrucker.db') as conn:
        c = conn.cursor()

        # בדוק אם העמודה first_name כבר קיימת, ואם לא - הוסף אותה
        try:
            c.execute('ALTER TABLE users ADD COLUMN first_name TEXT')
            print("Column 'first_name' added successfully.")
        except sqlite3.OperationalError:
            print("Column 'first_name' already exists.")

        conn.commit()


# קריאה לפונקציה לעדכון מסד הנתונים
update_db()


# קבלת שם פרטי של המשתמש
def get_first_name(username):
    with sqlite3.connect('GymTrucker.db') as conn:
        c = conn.cursor()
        c.execute("SELECT first_name FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        return result[0] if result else None


# בדיקה אם שם משתמש קיים
def user_exists(username):
    conn = sqlite3.connect('GymTrucker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None


# אימות משתמש וסיסמה
def authenticate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with sqlite3.connect('GymTrucker.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_password))
        return c.fetchone() is not None


# **חלק חדש - יצירת מסד נתונים אישי למשתמש**
def create_user_data_db(username):
    if not user_data_db_exists(username):  # בדיקה אם מסד הנתונים כבר קיים
        with sqlite3.connect(f'{username}_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS training_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    muscle_group TEXT NOT NULL
                )
            ''')
            conn.commit()


# בדיקה אם מסד נתונים אישי קיים
def user_data_db_exists(username):
    try:
        with sqlite3.connect(f'{username}_data.db') as conn:
            c = conn.cursor()
            c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="training_data"')
            return c.fetchone() is not None
    except Exception:
        return False


# הוספת נתון אימון למשתמש עם קבוצת שרירים
def add_training_entry(username, date, muscle_groups):
    if not isinstance(muscle_groups, list) or not all(isinstance(group, str) for group in muscle_groups):
        raise ValueError("Muscle groups must be a list of strings.")
    
    # בדוק אם קיים טבלה לאימונים, אם לא צור אותה
    validate_training_table(username)
    
    with sqlite3.connect(f'{username}_data.db') as conn:
        c = conn.cursor()
        # הוספת כל קבוצת שרירים עבור אותו אימון
        for group in muscle_groups:
            c.execute('INSERT INTO training_data (date, muscle_group) VALUES (?, ?)', (date, group))
        conn.commit()


# קבלת סיכום אימונים לפי קבוצות שרירים
def get_training_summary(username):
    validate_training_table(username)
    with sqlite3.connect(f'{username}_data.db') as conn:
        c = conn.cursor()
        c.execute('SELECT muscle_group, COUNT(*) FROM training_data GROUP BY muscle_group')
        data = c.fetchall()
        if not data:  # אם אין נתונים, החזר רשימה ריקה
            return []
        return data


# קבלת כל הנתונים לפי תאריכים
def get_training_dates(username):
    validate_training_table(username)
    with sqlite3.connect(f'{username}_data.db') as conn:
        c = conn.cursor()
        c.execute('SELECT date, muscle_group FROM training_data ORDER BY date DESC')
        return c.fetchall()


# עדכון טבלה של אימונים
def validate_training_table(username):
    with sqlite3.connect(f'{username}_data.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS training_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                muscle_group TEXT NOT NULL
            )
        ''')
        conn.commit()
from datetime import datetime, timedelta
import sqlite3

# פונקציה שמחזירה את מספר הפעמים שהתאמנת על כל קבוצת שרירים בשבוע האחרון
def get_training_count_last_week(username):
    # חישוב התאריך של שבוע אחורה
    last_week_date = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d")
    
    # יצירת מילון לשמירת תוצאות
    muscle_count = {muscle: 0 for muscle in ['Chest', 'Back', "Biceps", 'Triceps', "Front Shoulder", "Middle Shoulder", "Rear Shoulder", 'Legs']}
    
    # קישור למסד הנתונים של המשתמש
    with sqlite3.connect(f'{username}_data.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT muscle_group, COUNT(DISTINCT date)  -- נספר אימונים לפי שריר עם כל תאריך ייחודי
            FROM training_data 
            WHERE date >= ? 
            GROUP BY muscle_group
        ''', (last_week_date,))
        
        # קבלת התוצאות
        results = c.fetchall()
        
        # עדכון המילון עם הנתונים
        for muscle, count in results:
            muscle_count[muscle] = count
    
    return muscle_count
# יצירת טבלה חדשה לאימוני משקולות
def create_exercise_data_db(username):
    if not exercise_data_db_exists(username):  # בדיקה אם הטבלה כבר קיימת
        with sqlite3.connect(f'{username}_data.db') as conn:
            c = conn.cursor()
            c.execute(''' 
                CREATE TABLE IF NOT EXISTS exercise_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    muscle_group TEXT NOT NULL,
                    exercise TEXT NOT NULL,
                    num_set INTEGER NOT NULL,
                    reps INTEGER NOT NULL,
                    weight INTEGER NOT NULL
                )
            ''')
            conn.commit()
# בדיקה אם טבלת אימוני משקולות קיימת
def exercise_data_db_exists(username):
    try:
        with sqlite3.connect(f'{username}_data.db') as conn:
            c = conn.cursor()
            c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="exercise_data"')
            return c.fetchone() is not None
    except Exception:
        return False
# הוספת נתון אימון (תרגיל, מספר סטים, חזרות, משקל) למשתמש
def add_exercise_entry(username, date, muscle_group, exercise, num_set, reps, weight):
    if not isinstance(num_set, int) or not isinstance(reps, int) or not isinstance(weight, int):
        raise ValueError("Sets, reps, and weight must be integers.")
    
    # בדוק אם קיים טבלה לאימוני משקולות, אם לא צור אותה
    create_exercise_data_db(username)
    
    with sqlite3.connect(f'{username}_data.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO exercise_data (date, muscle_group, exercise, num_set, reps, weight) VALUES (?, ?, ?, ?, ?, ?)', 
                  (date, muscle_group, exercise, num_set, reps, weight))
        conn.commit()
# קבלת כל הנתונים לפי תאריכים ושרירים
def get_exercise_data(username):
    create_exercise_data_db(username)
    with sqlite3.connect(f'{username}_data.db') as conn:
        c = conn.cursor()
        c.execute('SELECT date, muscle_group, exercise, num_set, reps, weight FROM exercise_data ORDER BY date DESC')
        return c.fetchall()

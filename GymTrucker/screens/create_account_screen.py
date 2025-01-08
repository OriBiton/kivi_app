import re  # עבור ביטויים רגולריים
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from db import create_db, add_user, user_exists  # הוספת פונקציה לבדוק אם המשתמש קיים
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class CreateAccountScreen(Screen):
    # הגדרת התכונות עבור ה-IDs בקובץ ה-KV
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    email = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm_password = ObjectProperty(None)

    # פונקציה לבדיקה אם שם מכיל רק אותיות באנגלית
    def is_valid_name(self, name):
        return bool(re.match(r'^[A-Za-z]+$', name))  # רק אותיות באנגלית

    # פונקציה לבדיקה אם המייל תקין
    def is_valid_email(self, email):
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

    # פונקציה לבדיקה אם הסיסמה עומדת בתנאים
    def is_valid_password(self, password):
        if len(password) < 8:  # לפחות 8 תווים
            return False
        if not any(char.isupper() for char in password):  # לפחות אות גדולה אחת
            return False
        return True

    # פונקציה להצעת שם משתמש חלופי
    def suggest_alternative_username(self, username):
        count = 1
        new_username = username
        while user_exists(new_username):  # בדיקה אם השם קיים
            new_username = f"{username}{count}"
            count += 1
        return new_username

    def submit_form(self):
        create_db()  # יצירת מסד נתונים אם לא קיים

        # קבלת נתונים לאחר ניקוי רווחים מיותרים
        first_name = self.first_name.text.strip()
        last_name = self.last_name.text.strip()
        email = self.email.text.strip()
        username = self.username.text.strip()
        password = self.password.text.strip()
        confirm_password = self.confirm_password.text.strip()

        # בדיקות תקינות
        if not all([first_name, last_name, email, username, password, confirm_password]):
            self.show_popup("Please fill in all fields.")
            return

        if not self.is_valid_name(first_name) or not self.is_valid_name(last_name):
            self.show_popup("Names must contain only letters.")
            return

        if not self.is_valid_email(email):
            self.show_popup("Invalid email format.")
            return

        if not self.is_valid_password(password):
            self.show_popup("Password must be at least 8 characters with one uppercase letter.")
            return

        if password != confirm_password:
            self.show_popup("Passwords do not match!")
            return

        # בדיקת שם משתמש קיים
        if user_exists(username):
            alternative_username = self.suggest_alternative_username(username)
            self.show_popup(f"Username already exists. Try '{alternative_username}' instead.")
            return

        # ניסיון להוסיף משתמש
        try:
            add_user(username, password,first_name)
            self.show_popup("Account Created Successfully!")
            self.manager.current = 'login'
        except Exception as e:
            self.show_popup(f"Error: {str(e)}")

    # הצגת פופ-אפ
    def show_popup(self, message):
        popup = Popup(title="Notification", content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()

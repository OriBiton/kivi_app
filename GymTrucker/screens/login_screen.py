from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from db import authenticate_user
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class LoginScreen(Screen):
    # התאמה ל-IDs בקובץ ה-KV
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def login_user(self):
        # ניקוי רווחים מיותרים בקלט
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        # בדיקה שהשדות אינם ריקים
        if not all([username, password]):
            self.show_popup("Please fill in all fields.")
            return

        # אימות נתונים מול מסד הנתונים
       # הקוד במסך ה-login שלך
        if authenticate_user(username, password):
            self.show_popup("Login Successful!")
            # העברת שם המשתמש למסך 'EnteryScreen'
            entry_screen = self.manager.get_screen('entery')
            entry_screen.username = username  # העברת שם המשתמש
            entry_screen.on_enter()  # קריאה לפונקציה on_enter כדי לוודא שהמסך נטען כראוי
            self.manager.current = 'entery'

        else:
            self.show_popup("Invalid username or password")

    def show_popup(self, message):
        popup = Popup(title="Notification", content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()




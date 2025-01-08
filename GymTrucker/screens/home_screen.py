from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    # ניווט למסך ההתחברות
    def go_to_login(self):
        self.manager.current = 'login'

    # ניווט למסך יצירת החשבון
    def go_to_create_account(self):
        self.manager.current = 'create_account'

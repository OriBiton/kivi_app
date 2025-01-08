# main.py

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.login_screen import LoginScreen
from screens.create_account_screen import CreateAccountScreen
from screens.entery_screen import EnteryScreen
from screens.next_screen import NextScreen  # הוספת המסך החדש
from screens.review_analysis_screen import ReviewAnalysisScreen
from screens.workout_plan_screen import WorkoutPlanScreen  # הוספת מסך תוכנית האימון
from kivy.core.window import Window
Builder.load_file('kv_files/home_screen.kv')
Builder.load_file('kv_files/login_screen.kv')
Builder.load_file('kv_files/create_account_screen.kv')
Builder.load_file('kv_files/entery_screen.kv')
Builder.load_file("kv_files/Review_Analysis_screen.kv")
 # טעינת קובץ ה-KV של המסך החדש
Window.size = (400, 680)
class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CreateAccountScreen(name='create_account'))
        sm.add_widget(EnteryScreen(name='entery'))
        sm.add_widget(ReviewAnalysisScreen(name="review_analysis_screen"))
        sm.add_widget(NextScreen(name='next_screen')) 
        sm.add_widget(WorkoutPlanScreen(name='workout_plan_screen'))  # הוספת המסך החדש לתוך ה- ScreenManager
 # הוספת המסך החדש
        return sm

if __name__ == '__main__':
    MainApp().run()

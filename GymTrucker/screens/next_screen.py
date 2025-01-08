from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
import pandas as pd
from kivymd.uix.button import MDRaisedButton
# קריאת קובץ ה-CSV
df = pd.read_csv('Cleaned_Data.csv')

# יצירת המילון dct
dct = {}
for i in df.index:
    if df.loc[i, 'Target Muscle Group '] in dct.keys():
        dct[df.loc[i, 'Target Muscle Group ']].append(df.loc[i, '#NAME?'])
    else:
        dct[df.loc[i, 'Target Muscle Group ']] = [df.loc[i, '#NAME?']]

from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.metrics import dp

from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import OneLineListItem

from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import OneLineListItem
from kivy.metrics import dp  # שימוש במידות יחסיות

from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import OneLineListItem
from kivy.metrics import dp  # שימוש במידות יחסיות
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
import pandas as pd
from db import add_exercise_entry
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.properties import StringProperty
from datetime import datetime
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
class NextScreen(MDScreen):
    username = StringProperty("")
    selected_muscles = []  # השרירים שנבחרו במסך הקודם
    selected_exercises = []  # רשימה חדשה לתרגילים שנבחרו
    muscles_list = ['Chest', 'Back', "Biceps", 'Triceps', "Front Shoulder", "Middle Shoulder", "Rear Shoulder", 'Legs']
    dct = dct  # מילון עבור התרגילים

    def on_enter(self):
        
        self.clear_widgets()  # מנקה את המסך קודם
        self.md_bg_color = [0.2, 0.2, 0.2, 1]  # אפור כהה (RGBA)

        # יצירת שורת חיפוש עבור השרירים
        layout = GridLayout(cols=1, size_hint_y=None, height=Window.height * 0.1, size_hint_x=0.8)  # התאם גובה ורוחב
        # הוספת התמונה כרקע
        background_image = Image(source='images/background.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background_image)
        search_input = TextInput(
            hint_text="Search exercises...", 
            size_hint=(1, None), 
            height=Window.height * 0.08,  # גובה השדה 8% מהמסך
            pos_hint={"center_x": 0.5}  # מיקום במרכז
        )
        search_input.bind(text=self.on_text_change)  # חיבור לפונקציה כאשר הטקסט משתנה
        layout.add_widget(search_input)

        # יצירת ScrollView כדי לאפשר גלילה בתוצאות החיפוש
        self.results_layout = GridLayout(cols=1, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))

        results_scroll = ScrollView(size_hint=(1, None), height=Window.height * 0.3)  # גובה של 40% מהמסך
        results_scroll.add_widget(self.results_layout)

        layout.add_widget(results_scroll)

        # הצבת האלמנטים במעלה המסך
        layout.pos_hint = {'center_x': 0.5, 'top': 0.9}  # מיקום במעלה המסך
        self.add_widget(layout)

        # יצירת רשימת התרגילים דינמית
        self.create_exercise_list([])

        self.last_search = ''  # עיכוב חיפוש
        self.search_event = None

        # שמירה על התוצאות הקודמות כדי להימנע מחיפוש מיותר
        self.cached_results = {}

        # יצירת label חדש להצגת התרגילים שנבחרו
        self.selected_exercises_label = MDLabel(
            size_hint=(None, None),
            width=Window.width * 0.8,  # חצי מרוחב המסך
            halign='center',
            theme_text_color="Primary",  # הצבע הסגנוני
            text_color=(1, 0, 0, 1)  # צבע אדום (RGBA)
        )
        # הצבת ה-MDLabel במרכז של המסך (גם ב-X וגם ב-Y)
        self.selected_exercises_label.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # מיקום במרכז
        self.add_widget(self.selected_exercises_label)

        # יצירת כפתור Submit Program
        submit_button = MDRaisedButton(
            text="Submit Program", 
            size_hint=(None, None), 
            size=(Window.width * 3, Window.height * 0.1),  # כפתור תופס 60% רוחב ו-8% גובה
            pos_hint={'center_x': 0.8, 'top': 0.1},  # מיקום הכפתור במרכז
            on_release=self.submit_program  # חיבור לפונקציה של שליחה
        )
        self.add_widget(submit_button)

        # עדכון התצוגה עם התרגילים שנבחרו
        self.update_selected_exercises_display()

    def update_selected_exercises_display(self):
        """עדכון התצוגה של התרגילים שנבחרו"""
        self.selected_exercises_label.text = f"Selected exercises: {', '.join(self.selected_exercises)}"

    def on_text_change(self, instance, value):
        """פונקציה שתבצע חיפוש בזמן אמת עם עיכוב"""
        search_text = value.lower()  # המרת הטקסט לאותיות קטנות

        if self.search_event:
            # אם יש חיפוש קודם, נבטל אותו
            Clock.unschedule(self.search_event)

        # הצגת החיפוש אחרי 0.5 שניות (עיכוב)
        self.search_event = Clock.schedule_once(lambda dt: self.perform_search(search_text), 0.5)

    def perform_search(self, search_text):
        """ביצוע החיפוש בפועל אחרי עיכוב"""
        if search_text == self.last_search:
            return  # אם החיפוש לא השתנה, אין צורך לחפש מחדש

        self.last_search = search_text
        self.results_layout.clear_widgets()  # ניקוי תוצאות ישנות

        # אם התוצאות כבר קיימות בזיכרון, השתמש בהן ישירות
        if search_text in self.cached_results:
            exercises = self.cached_results[search_text]
        else:
            exercises = self.search_exercises(search_text)
            self.cached_results[search_text] = exercises

        # הצגת התרגילים שהמשתמש מקליד
        exercises_found = False
        for exercise in exercises:
            label = OneLineListItem(text=exercise)
            label.bind(on_release=self.create_add_exercise_function(exercise))  # חיבור לפונקציה לעיבוד הבחירה
            self.results_layout.add_widget(label)
            exercises_found = True

        if not exercises_found:
            no_results_label = OneLineListItem(text="No exercises found", size_hint_y=None, height=40)
            self.results_layout.add_widget(no_results_label)

    def search_exercises(self, search_text):
        """חיפוש התרגילים במילון הדינמי"""
        exercises = []
        for muscle in self.selected_muscles:
            muscle_exercises = self.dct.get(muscle, [])
            for exercise in muscle_exercises:
                if search_text in exercise.lower():
                    exercises.append(exercise)
        return exercises

    def create_exercise_list(self, exercises):
        """פונקציה שמייצרת רשימה של תרגילים עם אפשרות ללחוץ על כל תרגיל"""
        self.results_layout.clear_widgets()  # ניקוי תוצאות ישנות

        for exercise in exercises:
            item = OneLineListItem(text=exercise)
            item.bind(on_release=self.create_add_exercise_function(exercise))  # חיבור לפונקציה שנוצרה
            self.results_layout.add_widget(item)

    def create_add_exercise_function(self, exercise_name):
        """פונקציה שמחזירה פונקציה שתוסיף את התרגיל שנבחר"""
        def add_exercise(instance):
            if exercise_name not in self.selected_exercises:
                self.selected_exercises.append(exercise_name)
            self.update_selected_exercises_display()  # עדכון התצוגה
            print(f"Selected exercises: {', '.join(self.selected_exercises)}")  # הצגת התרגילים שנבחרו
        return add_exercise

    def submit_program(self, instance):
        """פונקציה שמבצעת את המעבר לעמוד הבא ושומרת את המילון"""
        # מילון חדש שנשמור לעמוד הבא
        
        exercise_muscle_mapping = {}

        # בניית מילון הפוך
        reverse_dct = {exercise: muscle for muscle, exercises in dct.items() for exercise in exercises}

        # חיבור תרגילים לשרירים
        for exercise in self.selected_exercises:
            if exercise in reverse_dct:
                exercise_muscle_mapping[exercise] = reverse_dct[exercise]

        # שלח את המילון לעמוד הבא
        workout_plan_screen = self.manager.get_screen('workout_plan_screen')  # השגת עמוד ה- workout_plan
        workout_plan_screen.set_exercise_muscle_mapping(exercise_muscle_mapping) 
        workout_plan_screen.username = self.username # הגדרת המילון

        self.manager.current = 'workout_plan_screen'  # מעבר לעמוד הבא

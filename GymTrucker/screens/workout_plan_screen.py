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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.properties import StringProperty
from datetime import datetime
from kivy.core.window import Window

class WorkoutPlanScreen(MDScreen):
    exercise_muscle_mapping = {}  # מילון שמכיל את התרגילים והשרירים
    sets_input_fields = {}  # שדות קלט עבור מספר הסטים
    reps_fields = {}  # שדות קלט עבור החזרות
    weights_fields = {}  # שדות קלט עבור המשקלים
    username = StringProperty("")

    def set_exercise_muscle_mapping(self, mapping):
        """עדכון המילון של exercise_muscle_mapping"""
        self.exercise_muscle_mapping = mapping

    def on_enter(self):
        self.clear_widgets()  # מנקה את המסך קודם

        # יצירת ScrollView ראשי שיתפוס 90% מהמסך
        main_scroll_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))  # המרווחים בין התרגילים יותר קטנים
        main_scroll_layout.bind(minimum_height=main_scroll_layout.setter('height'))
        main_scroll_view = ScrollView(size_hint=(1, 0.9), pos_hint={"x": 0.05, "top": 1})
        main_scroll_view.add_widget(main_scroll_layout)
        self.add_widget(main_scroll_view)

        # עבור כל תרגיל במילון
        for exercise, muscle in self.exercise_muscle_mapping.items():
            # יצירת כותרת לתרגיל ושריר (נמצאת קרוב לשמאל עם ריווח פנימי)
            label = MDLabel(
                text=f"{exercise} ({muscle})",
                halign="left",
                theme_text_color="Primary",
                size_hint_y=None,
                height=Window.height * 0.05,  # תופס 5% מגובה המסך
                pos_hint={"x": 0.1}  # שמתי את הכותרת יותר פנימה
            )
            main_scroll_layout.add_widget(label)

            # יצירת ScrollView פנימי עבור הסטים, חזרות ומשקלים
            exercise_scroll_layout = GridLayout(cols=1, size_hint_y=None)
            exercise_scroll_layout.bind(minimum_height=exercise_scroll_layout.setter('height'))
            exercise_scroll_view = ScrollView(size_hint=(1, None), height=Window.height * 0.5)  # תופס חצי גובה המסך
            exercise_scroll_view.add_widget(exercise_scroll_layout)

            # שדה קלט לבחירת מספר הסטים
            sets_input = MDTextField(
                hint_text="Enter number of sets",
                size_hint=(None, None),
                width=Window.width * 0.6,  # תופס 70% מהמסך
                
                height=dp(40),
                pos_hint={"center_x": 0.5}  # מתאים יחסית למרכז המסך
            )
            sets_input.exercise_name = exercise  # שמירת שם התרגיל בשדה הקלט
            sets_input.bind(on_text_validate=lambda instance: self.on_sets_entered(instance))
            self.sets_input_fields[exercise] = sets_input  # שומר את השדה לפי שם התרגיל
            exercise_scroll_layout.add_widget(sets_input)

            main_scroll_layout.add_widget(exercise_scroll_view)

        # כפתור Submit
        submit_button = MDRaisedButton(
            text="Submit Program",
            size_hint=(None, None),
            size=(Window.width * 0.3, Window.height * 0.1),  # כפתור תופס 60% רוחב ו-10% גובה
            pos_hint={"center_x": 0.8,'center_y':0.1},  # ממקם במרכז
            on_release=self.submit_program
        )
        self.add_widget(submit_button)

    def on_sets_entered(self, instance):
        """פונקציה שתופעל כאשר מספר הסטים נכנס"""
        exercise = instance.exercise_name  # מזהה את שם התרגיל מתוך השדה
        sets_count = instance.text  # מספר הסטים שהוזן

        try:
            sets_count = int(sets_count)
            if sets_count > 0:  # לוודא שהמשתמש הכניס מספר סטים תקני
                print(f"Sets count entered for {exercise}: {sets_count}")  # הדפסת מספר הסטים
                # יצירת שדות חזרות ומשקלים עבור תרגיל זה בלבד
                self.create_reps_weight_fields(exercise, sets_count, instance.parent)
            else:
                print(f"Invalid sets count for {exercise}: {sets_count}")  # הדפסת הודעת שגיאה
        except ValueError:
            print(f"ValueError for {exercise} - invalid input: {sets_count}")  # הדפסת שגיאה

    def create_reps_weight_fields(self, exercise, sets_count, exercise_scroll_layout):
        """יצירת שדות קלט לחזרות ולמשקלים לפי מספר הסטים"""
        # קודם כל נמחק את השדות הקודמים אם היו
        if exercise in self.reps_fields:
            for rep_field in self.reps_fields[exercise]:
                exercise_scroll_layout.remove_widget(rep_field)
            for weight_field in self.weights_fields[exercise]:
                exercise_scroll_layout.remove_widget(weight_field)

        # יצירת שדות חזרות ומשקלים
        self.reps_fields[exercise] = []
        self.weights_fields[exercise] = []

        for i in range(sets_count):
            # BoxLayout אופקי להצגת חזרות ומשקלים אחד ליד השני
            box_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))

            # שדה קלט עבור חזרות
            reps_input = MDTextField(
                hint_text=f"Reps for Set {i + 1}",
                size_hint=(None, None),
                width=Window.width * 0.4,  # תופס 40% מהרוחב
                height=dp(40),
                pos_hint={"center_x": 0.3}
            )
            self.reps_fields[exercise].append(reps_input)
            box_layout.add_widget(reps_input)

            # שדה קלט עבור משקלים
            weight_input = MDTextField(
                hint_text=f"Weight for Set {i + 1}",
                size_hint=(None, None),
                width=Window.width * 0.4,  # תופס 40% מהרוחב
                height=dp(40),
                pos_hint={"center_x": 0.7}  
            )
            self.weights_fields[exercise].append(weight_input)
            box_layout.add_widget(weight_input)

            # הוספת ה-BoxLayout לתוך ה-ScrollLayout
            exercise_scroll_layout.add_widget(box_layout)

        # עדכון הגובה של ה-scroll layout אחרי הוספת השדות
        exercise_scroll_layout.height = len(self.reps_fields[exercise]) * dp(50)
        self.update_scrollview(exercise_scroll_layout)

    def update_scrollview(self, scroll_layout):
        """עדכון גובה ה-scrollview באופן דינמי"""
        scroll_layout.height = max(500, scroll_layout.height)

    def submit_program(self, instance):
        """פונקציה לשלוח את המידע למערכת ולשמור ב-DB"""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # השגת תאריך נוכחי
        
        for exercise in self.exercise_muscle_mapping.keys():
            reps = [reps.text for reps in self.reps_fields.get(exercise, [])]
            weights = [weights.text for weights in self.weights_fields.get(exercise, [])]
            muscle_group = self.exercise_muscle_mapping[exercise]  # שריר קשור לתרגיל
            sets = int(self.sets_input_fields[exercise].text)  # מספר הסטים שהוזן
            
            for i in range(sets):
                try:
                    # המרת כל הערכים ל-int
                    reps_value = int(reps[i])
                    weights_value = int(weights[i])
                    
                    # הוספת שורה חדשה למסד הנתונים
                    add_exercise_entry(self.username, date, muscle_group, exercise, i + 1, reps_value, weights_value)  # העברת מספר הסט בשדה 'sets' 
                    
                except ValueError:
                    print(f"Invalid input for Set {i + 1} of {exercise}: Sets, reps, and weight must be integers.")
                    return  # עצור אם יש ערך לא חוקי
        print(f"Data for {self.username} saved successfully!")

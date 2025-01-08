import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class ExerciseSearchApp(App):

    def build(self):
        # טוען את הנתונים מקובץ ה-CSV
        self.df = pd.read_csv('Exercises.csv')  # הנתיב לקובץ שלך
        
        # יצירת תפריט חיפוש
        self.layout = BoxLayout(orientation='vertical')

        # רשימת השרירים שנבחרו
        self.selected_muscles = ['Legs', 'Back']  # לדוגמה

        # יצירת ScrollView שיכיל את כל שורות החיפוש
        self.search_layout = ScrollView()
        self.search_grid = GridLayout(cols=1, size_hint_y=None)
        self.search_grid.bind(minimum_height=self.search_grid.setter('height'))
        
        # יצירת שדה חיפוש לכל שריר שנבחר
        for muscle in self.selected_muscles:
            # יצירת שדה חיפוש לכל שריר
            search_input = TextInput(hint_text=f'חפש תרגילים ל-{muscle}', size_hint_y=None, height=40)
            search_input.bind(on_text_validate=self.on_search)  # trigger when user presses enter
            search_input.muscle_name = muscle  # נשמור את שם השריר בשדה החיפוש
            self.search_grid.add_widget(search_input)
        
        # הוספת GridLayout לתוך ScrollView
        self.search_layout.add_widget(self.search_grid)

        # הוספת את ה-ScrollView ללayout
        self.layout.add_widget(self.search_layout)

        # רשימה של תרגילים שנבחרו
        self.selected_exercises = []

        return self.layout

    def on_search(self, instance):
        # קבלת מילה שהוקלדה בשדה החיפוש
        search_term = instance.text.lower()
        muscle = instance.muscle_name  # השריר שהוקלד עבורו שדה החיפוש

        # סינון התרגילים לפי השריר והחיפוש
        matching_exercises = self.df[(self.df['Target Muscle Group '].str.lower() == muscle.lower()) & 
                                     (self.df['#NAME?'].str.contains(search_term, case=False))]

        # הצגת תוצאות החיפוש
        self.display_search_results(matching_exercises)

    def display_search_results(self, exercises):
        # נקה את התוצאות הקודמות
        self.search_grid.clear_widgets()

        # הצגת שדות חיפוש מחדש (כדי לשמור על השרירים שהוספו)
        for muscle in self.selected_muscles:
            search_input = TextInput(hint_text=f'חפש תרגילים ל-{muscle}', size_hint_y=None, height=40)
            search_input.bind(on_text_validate=self.on_search)
            search_input.muscle_name = muscle  # נשמור את שם השריר בשדה החיפוש
            self.search_grid.add_widget(search_input)

        # הצגת תוצאות חיפוש עם CheckBox לכל תרגיל
        for exercise in exercises.itertuples():
            exercise_name = exercise[1]  # שם התרגיל
            checkbox = CheckBox(active=False)
            checkbox.bind(on_active=self.on_checkbox_active)
            label = Label(text=exercise_name)
            self.search_grid.add_widget(label)
            self.search_grid.add_widget(checkbox)

    def on_checkbox_active(self, instance, value):
        # הוספת או הסרת תרגילים מהרשימה
        if value:
            self.selected_exercises.append(instance.parent.children[1].text)
        else:
            self.selected_exercises.remove(instance.parent.children[1].text)

    def display_selected_exercises(self, instance):
        # הצגת התרגילים שנבחרו
        print("תרגילים נבחרים:", self.selected_exercises)



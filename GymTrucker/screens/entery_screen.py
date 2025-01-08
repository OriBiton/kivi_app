from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox  # ייבוא הנכון של ה-checkbox
from db import get_first_name, add_training_entry
from datetime import datetime
from kivy.core.window import Window

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton
import matplotlib.pyplot as plt
from db import get_first_name, add_training_entry,get_training_count_last_week
# פונקציה שמציגה את הגרף

    
import matplotlib.pyplot as plt
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image as CoreImage
import io

from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from db import get_first_name, add_training_entry, get_training_count_last_week
from datetime import datetime
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from db import get_training_count_last_week

from kivy.graphics import Rectangle, Color


from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label  # Import רגיל של Label לצורך הצגת טקסט מעל הגרף

from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label  # Import רגיל של Label לצורך הצגת טקסט

from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label  # Import רגיל של Label לצורך הצגת טקסט

from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label  # Import רגיל של Label לצורך הצגת טקסט



from kivy.properties import StringProperty



# מסך שמציג את הגרף
class EnteryScreen(MDScreen):
    username = StringProperty("")  # הוספת username כפרופרטי
    first_name = StringProperty("")  # שם פרטי של המשתמש שיתעדכן
    selected_muscles = []  # רשימה לאחסון השרירים שנבחרו
    current_program = ""
    muscles_list = ['Chest', 'Back', "Biceps",'Triceps', "Front Shoulder", "Middle Shoulder","Rear Shoulder", 'Legs']
    
    

    
    def go_to_review_analysis_screen(self):
        # שים לב שאנחנו מעבירים את שם המשתמש למסך הבא
        review_screen = self.manager.get_screen('review_analysis_screen')
        review_screen.username = self.username  # שמור את שם המשתמש כאן
        self.manager.current = 'review_analysis_screen'  # המעבר למסך החדש

    def on_enter(self):
        self.md_bg_color = [0.2, 0.2, 0.2, 1]  # אפור כהה (RGBA)
        print(f"Entered EnteryScreen with username: {self.username}")  # הדפסת שם המשתמש לווידוא

        if self.username:
            self.first_name = get_first_name(self.username)
            if self.first_name:
                self.ids.welcome_label.text = f"Welcome back {self.first_name}"

            

            # עדכון מיקום הגרף אחרי טעינת המסך
            

    
    
    def toggle_muscle_selection(self, muscle):
        # אם השריר כבר נבחר, נסיר אותו, אחרת נוסיף אותו לרשימה
        if muscle in self.selected_muscles:
            self.selected_muscles.remove(muscle)
        else:
            self.selected_muscles.append(muscle)

        self.update_menu_items()  # עדכון פריטי התפריט

    def update_menu_items(self):
        # עדכון המראה של כל פריט בתפריט לפי אם הוא נבחר או לא
        for item in self.menu.items:
            if isinstance(item, OneLineListItem):  # אם מדובר בפריט מסוג OneLineListItem
                if item.text in self.selected_muscles:
                    item.text_color = (0.3, 0.3, 0.3, 1)  # צבע כהה לשרירים שנבחרו
                else:
                    item.text_color = (0, 0, 0, 1)  # צבע רגיל לשרירים שלא נבחרו

        # עדכון השורה עם השרירים שנבחרו
        self.ids.muscle_selection_label.text = f"Selected muscles: {', '.join(self.selected_muscles)}"

    def start_training(self):
        date = datetime.now().strftime("%Y-%m-%d")
        if self.selected_muscles:
            add_training_entry(self.username, date, self.selected_muscles)
            print("Training data saved:", self.selected_muscles)
            next_screen = self.manager.get_screen('next_screen')  # עדכון שם המסך
            next_screen.selected_muscles = self.selected_muscles
            next_screen.username = self.username  # העברת שם המשתמש
            print("Muscles to be displayed on next screen:", next_screen.selected_muscles)  # העברת השרירים למסך הבא
            self.manager.current = 'next_screen'  # מעבר למסך הבא
        else:
            print("No muscles selected.")


    def open_muscle_list(self):
        # יצירת רשימת פריטים ל-MDDropdownMenu
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": muscle,
                "on_release": lambda x=muscle: self.toggle_muscle_selection(x)
            } for muscle in self.muscles_list
        ]

        # יצירת ה-MDDropdownMenu
        self.menu = MDDropdownMenu(
            caller=self.ids.muscle_button,  # הכפתור שיפתח את התפריט
            items=menu_items,
            width_mult=4,
            max_height=200,
            position="center"  # גובה מקסימלי של התפריט
        )
        self.menu.open()
     # המפה שמכילה את השרירים עבור כל תכנית אימון
    training_map = {
        "Back & Chest": ["Back", "Chest"],
        "Shoulders & Arms": ["Shoulders", "Biceps",'Triceps'],
        "Legs": ["Legs"],
        "Push": ["Chest", "Triceps", "Front Shoulder", "Middle Shoulder"],
        "Pull": ["Back", "Biceps", "Rear Shoulder"],
        "Chest": ["Chest"],
        "Arms": ["Biceps",'Triceps'],
        "Shoulders": ["Front Shoulder", "Middle Shoulder","Rear Shoulder"],
        "Back": ["Back"]
    }

    
    

    def select_training(self, program):
        # אם התכנית שנבחרה כבר קיימת, נמחק את השרירים שלה
        if self.current_program == program:
            muscles_to_remove = self.training_map[program]
            for muscle in muscles_to_remove:
                if muscle in self.selected_muscles:
                    self.selected_muscles.remove(muscle)
            self.ids.muscle_selection_label.text = f"Selected Program: | Selected Muscles: "
            self.current_program = ""  # מבטלים את הבחירה בתכנית
            print(f"Program {program} deselected.")
        else:
            # אם נבחרה תכנית אחרת, נוודא שנמחקים השרירים של התכנית הקודמת
            if self.current_program:
                muscles_to_remove = self.training_map[self.current_program]
                for muscle in muscles_to_remove:
                    if muscle in self.selected_muscles:
                        self.selected_muscles.remove(muscle)
            
            # שמירת השרירים הנבחרים מתוך המפה בהתאם לתכנית האימון החדשה
            muscles_to_add = self.training_map[program]
            self.selected_muscles.extend(muscles_to_add)
            self.ids.muscle_selection_label.text = f"Selected Program: {program} | Selected Muscles: {', '.join(self.selected_muscles)}"
            self.current_program = program  # עדכון לתכנית הנוכחית
            print(f"Program {program} selected.")

    def build_training_buttons(self):
        # יצירת כפתורים עבור תכניות האימון הפופולריות
        training_buttons = [
            ("Back & Chest", self.select_training),
            ("Shoulders & Arms", self.select_training),
            ("Legs", self.select_training),
            ("Push", self.select_training),
            ("Pull", self.select_training),
            ("Chest", self.select_training),
            ("Arms", self.select_training),
            ("Shoulders", self.select_training),
            ("Back", self.select_training)
        ]
        
        # יצירת הכפתורים בפורמט של GridLayout
        button_layout = BoxLayout(orientation='vertical', spacing=10)
        for i in range(0, len(training_buttons), 3):  # 3 כפתורים בשורה
            row_layout = BoxLayout(orientation='horizontal', spacing=10)
            for label, action in training_buttons[i:i + 3]:
                button = MDRaisedButton(
                    text=label,
                    on_press=lambda instance, label=label: action(label)  # שמירה על הערך של label
                )
                row_layout.add_widget(button)
            button_layout.add_widget(row_layout)
        
        self.ids.training_buttons_container.add_widget(button_layout)
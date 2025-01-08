import os
import matplotlib.pyplot as plt
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from db import get_training_count_last_week
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock  # להוסיף את הכלי של השעון

class ReviewAnalysisScreen(MDScreen):
    username = StringProperty("")  # הגדרת username
    img = None  # אתחול משתנה לתמונה

    def on_enter(self):
        self.display_graph()  # הצגת הגרף ברגע שהמסך נטען

    def display_graph(self):
        # שליפת נתוני האימונים מהשבוע האחרון
        muscle_count = get_training_count_last_week(self.username)
        muscles = list(muscle_count.keys())
        counts = list(muscle_count.values())

        # יצירת גרף עמודות עם Matplotlib
        fig, ax = plt.subplots(figsize=(10, 8))  # הגדלת הגרף

        ax.bar(muscles, counts, color='blue')

        # הגדרת כותרות
        ax.set_title("Training Analysis (Last Week)")
        ax.set_xlabel("Muscle Group")
        ax.set_ylabel("Number of Workouts")

        # סיבוב שמות ציר ה-X ב-45 מעלות והוספת מרווחים נוספים
        plt.xticks(rotation=45, ha='right', rotation_mode='anchor')

        # הגדרת נתיב לתיקיית העבודה של הקוד
        current_directory = os.path.dirname(os.path.abspath(__file__))  # תיקיית העבודה של הקוד
        image_path = os.path.join(current_directory, 'training_analysis.png')  # שמירה בתיקיית העבודה של הקוד

        # שמירה כקובץ תמונה
        fig.savefig(image_path, bbox_inches='tight')  # שמירה עם מרווחים כדי למנוע חיתוך

        # יצירת וידג'ט של תמונה
        self.img = Image(source=image_path)
        self.img.size_hint = (None, None)  # לא נעשה שימוש ב-size_hint באופן אוטומטי

        # עדכון המידות באופן דינמי בהתאם לגודל המסך
        Clock.schedule_once(self.update_image_size)

        # הוספת התמונה לווידג'ט
        self.ids.graph_container.clear_widgets()
        self.ids.graph_container.add_widget(self.img)

    def update_image_size(self, *args):
        # עדכון הגודל של התמונה
        self.img.size = (self.width * 0.8, self.height * 0.6)  # גודל דינמי שמתאים לגודל המסך
        self.img.pos = ((self.width - self.img.width) / 2, (self.height - self.img.height) / 2)  # ממקם את התמונה במרכז

    def go_back_to_entry_screen(self):
        # מעבר למסך הקודם (המסך שבו נמצא ה-EnteryScreen)
        self.manager.current = 'entery'

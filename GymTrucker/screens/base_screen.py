import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout

# נתיבים לקבצים
LOGO_PATH = 'images/logo.png'
BACKGROUND_PATH = 'images/background.jpg'

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # הגדרת רקע לכל המסכים
        with self.canvas.before:
            self.bg = kivy.graphics.Rectangle(
                source=BACKGROUND_PATH,
                size=self.size,
                pos=self.pos
            )

        # עדכון מיקום הרקע בזמן שינוי גודל
        self.bind(size=self.update_bg, pos=self.update_bg)

        # הוספת לוגו בפינה השמאלית העליונה
        anchor_layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=[10, 10])
        logo = Image(source=LOGO_PATH, size_hint=(None, None), size=(250, 250))
        anchor_layout.add_widget(logo)
        self.add_widget(anchor_layout)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
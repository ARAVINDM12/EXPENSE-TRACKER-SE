import os
import sys
import ctypes
import threading
import subprocess

# Calculate screen center using ctypes before importing Kivy
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

window_width = 500
window_height = 400

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set window position before Kivy starts
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

# Kivy config
from kivy.config import Config
Config.set('graphics', 'width', str(window_width))
Config.set('graphics', 'height', str(window_height))
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

class SplashApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)

        self.layout = FloatLayout()

        # Splash image
        splash_image = Image(
            source="ExpenseApp/Images/SS.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        # Loading label (animated)
        self.loading_label = Label(
            text="Loading",
            font_size="20sp",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "y": 0.05}
        )

        self.dots = 0
        Clock.schedule_interval(self.update_loading_text, 0.5)

        self.layout.add_widget(splash_image)
        self.layout.add_widget(self.loading_label)

        return self.layout

    def update_loading_text(self, dt):
        # Cycle through Loading., Loading.., Loading...
        self.dots = (self.dots + 1) % 5
        self.loading_label.text = "Loading" + "." * self.dots

    def on_start(self):
        # Load app in background thread
        self.app_thread = threading.Thread(target=self.load_main_app)
        self.app_thread.start()

        # Close splash after delay
        Clock.schedule_once(self.close_splash, 7.5)

    def load_main_app(self):
        self.app_process = subprocess.Popen([sys.executable, os.path.abspath("ExpenseApp/main.py")])

    def close_splash(self, dt):
        self.stop()

if __name__ == "__main__":
    SplashApp().run()

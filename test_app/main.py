from kivy.config import Config

Config.set("graphics", "width", "390")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", True)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from storage_manager import store
from screens.consent_screen import ConsentScreen
from screens.profile_screen import ProfileScreen
from screens.result_screen import ResultScreen
from screens.compatibility_screen import CompatibilityScreen


Window.softinput_mode = "resize"


class ZodiacApp(App):
    def build(self):
        manager = ScreenManager()

        manager.add_widget(ConsentScreen(name="consent"))
        manager.add_widget(ProfileScreen(name="profile"))
        manager.add_widget(ResultScreen(name="result"))
        manager.add_widget(CompatibilityScreen(name="compatibility"))

        if store.exists("consent"):
            if store.exists("user"):
                manager.current = "result"
                manager.get_screen("result").show_profile()
            else:
                manager.current = "profile"
        else:
            manager.current = "consent"

        return manager


ZodiacApp().run()

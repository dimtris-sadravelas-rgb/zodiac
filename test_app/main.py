from kivy.config import Config

Config.set("graphics", "width", "390")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", True)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

Window.softinput_mode = "resize"


class ZodiacApp(App):
    def build(self):
        try:
            from kivy.uix.screenmanager import ScreenManager
            from storage_manager import store
            from screens.consent_screen import ConsentScreen
            from screens.profile_screen import ProfileScreen
            from screens.result_screen import ResultScreen
            from screens.compatibility_screen import CompatibilityScreen

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

        except Exception as error:
            import traceback

            text = traceback.format_exc()

            label = Label(
                text=text,
                font_size=16,
                halign="left",
                valign="top",
                text_size=(Window.width - 20, None),
                size_hint_y=None
            )

            label.bind(
                texture_size=lambda instance, value:
                setattr(instance, "height", value[1] + 40)
            )

            scroll = ScrollView()
            scroll.add_widget(label)
            return scroll


ZodiacApp().run()

import webbrowser

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image

from helpers import fs, make_label
from storage_manager import store, get_font_extra, set_font_extra
from zodiac_data import ZODIACS


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main = BoxLayout(orientation="vertical")
        self.add_widget(self.main)

    def show_profile(self):
        self.main.clear_widgets()

        user = store.get("user")
        zodiac_name = user["zodiac"]
        data = ZODIACS[zodiac_name]

        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation="vertical", padding=20, spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)

        content.add_widget(make_label(f"{user['first_name']} {user['last_name']}", 27, height=55, bold=True))
        content.add_widget(make_label(f"Ηλικία: {user['age']} | Ζώδιο: {zodiac_name}", 23, height=55, bold=True))

        content.add_widget(Image(
            source=data["image"],
            size_hint_y=None,
            height=260,
            allow_stretch=True,
            keep_ratio=True
        ))

        content.add_widget(make_label("Προφίλ ζωδίου", 25, height=50, bold=True))
        content.add_widget(make_label(data["text"], 21))

        content.add_widget(make_label("Βασικά στοιχεία", 25, height=50, bold=True))
        content.add_widget(make_label(
            f"Στοιχείο: {data['element']}\n"
            f"Τυχερό χρώμα: {data['color']}\n"
            f"Τυχερός αριθμός: {data['number']}",
            21
        ))

        content.add_widget(make_label("Δυνατά σημεία", 25, height=50, bold=True))
        content.add_widget(make_label(data["strengths"], 21))

        content.add_widget(make_label("Αδυναμίες", 25, height=50, bold=True))
        content.add_widget(make_label(data["weaknesses"], 21))

        content.add_widget(make_label("Ημερήσιο μήνυμα", 25, height=50, bold=True))
        content.add_widget(make_label(data["daily"], 21))

        content.add_widget(make_label("Πιο συμβατά ζώδια", 25, height=50, bold=True))

        for sign in data["compatible"]:
            btn = Button(
                text=sign,
                font_size=fs(22),
                size_hint_y=None,
                height=65,
                background_color=(0.2, 0.55, 0.25, 1)
            )
            btn.bind(on_press=lambda instance, s=sign: self.open_compatibility(zodiac_name, s, True))
            content.add_widget(btn)

        content.add_widget(make_label("Λιγότερο συμβατά ζώδια", 25, height=50, bold=True))

        for sign in data["difficult"]:
            btn = Button(
                text=sign,
                font_size=fs(22),
                size_hint_y=None,
                height=65,
                background_color=(0.65, 0.25, 0.25, 1)
            )
            btn.bind(on_press=lambda instance, s=sign: self.open_compatibility(zodiac_name, s, False))
            content.add_widget(btn)

        link = Button(
            text="Άνοιγμα online ανάλυσης",
            font_size=fs(22),
            size_hint_y=None,
            height=65
        )
        link.bind(on_press=lambda instance: webbrowser.open(data["link"]))
        content.add_widget(link)

        edit = Button(
            text="Αλλαγή στοιχείων",
            font_size=fs(22),
            size_hint_y=None,
            height=65
        )
        edit.bind(on_press=lambda instance: setattr(self.manager, "current", "profile"))
        content.add_widget(edit)

        zoom_row = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=60)

        smaller = Button(text="A-", font_size=fs(22))
        bigger = Button(text="A+", font_size=fs(22))

        smaller.bind(on_press=lambda instance: self.change_font(-2))
        bigger.bind(on_press=lambda instance: self.change_font(2))

        zoom_row.add_widget(smaller)
        zoom_row.add_widget(bigger)
        content.add_widget(zoom_row)

        self.main.add_widget(scroll)

    def change_font(self, amount):
        new_value = get_font_extra() + amount
        new_value = max(-4, min(new_value, 12))
        set_font_extra(new_value)
        self.show_profile()

    def open_compatibility(self, my_sign, other_sign, is_good):
        screen = self.manager.get_screen("compatibility")
        screen.show(my_sign, other_sign, is_good)
        self.manager.current = "compatibility"

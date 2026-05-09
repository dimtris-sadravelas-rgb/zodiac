from datetime import date

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button

from helpers import fs, make_label, calculate_age, find_zodiac
from storage_manager import store, get_font_extra, set_font_extra


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical")
        self.add_widget(root)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=14,
            size_hint_y=None
        )
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)

        self.content.add_widget(make_label("Στοιχεία Χρήστη", 30, height=65, bold=True))

        self.first_name = TextInput(
    hint_text="Όνομα",
    multiline=False,
    font_size=fs(23),
    size_hint_y=None,
    height=65,
    write_tab=False,
    keyboard_suggestions=False
)
        self.content.add_widget(self.first_name)
        self.first_name.bind(
            focus=lambda instance, value:
            self.scroll_to_input(instance, value)
        )

        self.last_name = TextInput(
    hint_text="Επίθετο",
    multiline=False,
    font_size=fs(23),
    size_hint_y=None,
    height=65,
    write_tab=False,
    keyboard_suggestions=False
)
        self.content.add_widget(self.last_name)
        self.last_name.bind(
            focus=lambda instance, value:
            self.scroll_to_input(instance, value)
        )

        self.gender = Spinner(
            text="Φύλο",
            values=["Άνδρας", "Γυναίκα", "Άλλο / Δεν απαντώ"],
            font_size=fs(22),
            size_hint_y=None,
            height=65
        )
        self.content.add_widget(self.gender)

        self.content.add_widget(make_label("Ημερομηνία γέννησης", 22, height=45, bold=True))

        self.date_input = TextInput(
    hint_text="π.χ. 25/03/2000",
    multiline=False,
    font_size=fs(23),
    size_hint_y=None,
    height=65,
    write_tab=False,
    keyboard_suggestions=False,
    input_type="number"
)
        self.content.add_widget(self.date_input)
        self.date_input.bind(
            focus=lambda instance, value:
            self.scroll_to_input(instance, value)
        )

        row = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=65)

        self.day_spinner = Spinner(
            text="Ημέρα",
            values=[str(i) for i in range(1, 32)],
            font_size=fs(18)
        )

        self.month_spinner = Spinner(
            text="Μήνας",
            values=[str(i) for i in range(1, 13)],
            font_size=fs(18)
        )

        self.year_spinner = Spinner(
            text="Χρονιά",
            values=[str(i) for i in range(date.today().year, 1900, -1)],
            font_size=fs(18)
        )

        row.add_widget(self.day_spinner)
        row.add_widget(self.month_spinner)
        row.add_widget(self.year_spinner)
        self.content.add_widget(row)

        self.error = Label(
            text="",
            color=(1, 0.2, 0.2, 1),
            font_size=fs(18),
            size_hint_y=None,
            height=55
        )
        self.content.add_widget(self.error)

        submit = Button(
            text="Βρες το Ζώδιό μου",
            font_size=fs(24),
            size_hint_y=None,
            height=70
        )
        submit.bind(on_press=self.submit)
        self.content.add_widget(submit)

        clear = Button(
            text="Καθαρισμός στοιχείων",
            font_size=fs(21),
            size_hint_y=None,
            height=60
        )
        clear.bind(on_press=self.clear_user)
        self.content.add_widget(clear)

        terms = Button(
            text="Προβολή όρων",
            font_size=fs(21),
            size_hint_y=None,
            height=60
        )
        terms.bind(on_press=self.show_terms)
        self.content.add_widget(terms)

        zoom_row = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=60)

        smaller = Button(text="A-", font_size=fs(22))
        bigger = Button(text="A+", font_size=fs(22))

        smaller.bind(on_press=lambda instance: self.change_font(-2))
        bigger.bind(on_press=lambda instance: self.change_font(2))

        zoom_row.add_widget(smaller)
        zoom_row.add_widget(bigger)

        self.content.add_widget(zoom_row)

    def scroll_to_input(self, widget, focused):
        if focused:
            Clock.schedule_once(
                lambda dt: self.scroll.scroll_to(widget, padding=220),
                0.5
            )

    def on_enter(self):
        if store.exists("user"):
            user = store.get("user")
            self.first_name.text = user.get("first_name", "")
            self.last_name.text = user.get("last_name", "")
            self.gender.text = user.get("gender", "Φύλο")
            self.date_input.text = user.get("birth_date_text", "")

    def change_font(self, amount):
        new_value = get_font_extra() + amount
        new_value = max(-4, min(new_value, 12))
        set_font_extra(new_value)
        self.manager.current = "profile"

    def show_terms(self, instance):
        self.manager.current = "consent"

    def clear_user(self, instance):
        if store.exists("user"):
            store.delete("user")

        self.first_name.text = ""
        self.last_name.text = ""
        self.gender.text = "Φύλο"
        self.date_input.text = ""
        self.day_spinner.text = "Ημέρα"
        self.month_spinner.text = "Μήνας"
        self.year_spinner.text = "Χρονιά"
        self.error.text = "Τα στοιχεία καθαρίστηκαν."

    def submit(self, instance):
        first_name = self.first_name.text.strip()
        last_name = self.last_name.text.strip()
        gender = self.gender.text

        if first_name == "" or last_name == "":
            self.error.text = "Συμπλήρωσε όνομα και επίθετο."
            return

        if gender == "Φύλο":
            self.error.text = "Διάλεξε φύλο."
            return

        birth_date = self.get_birth_date()

        if birth_date is None:
            return

        if birth_date > date.today():
            self.error.text = "Η ημερομηνία γέννησης δεν μπορεί να είναι στο μέλλον."
            return

        age = calculate_age(birth_date)
        zodiac_name = find_zodiac(birth_date.month, birth_date.day)

        if zodiac_name is None:
            self.error.text = "Δεν βρέθηκε ζώδιο."
            return

        birth_date_text = f"{birth_date.day:02d}/{birth_date.month:02d}/{birth_date.year}"

        store.put(
            "user",
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_date_text=birth_date_text,
            zodiac=zodiac_name,
            age=age
        )

        result = self.manager.get_screen("result")
        result.show_profile()
        self.manager.current = "result"

    def get_birth_date(self):
        typed = self.date_input.text.strip()

        if typed != "":
            try:
                day, month, year = typed.split("/")
                return date(int(year), int(month), int(day))
            except ValueError:
                self.error.text = "Λάθος μορφή. Γράψε π.χ. 25/03/2000"
                return None

        if (
            self.day_spinner.text == "Ημέρα"
            or self.month_spinner.text == "Μήνας"
            or self.year_spinner.text == "Χρονιά"
        ):
            self.error.text = "Συμπλήρωσε ημέρα, μήνα και χρονιά."
            return None

        try:
            return date(
                int(self.year_spinner.text),
                int(self.month_spinner.text),
                int(self.day_spinner.text)
            )
        except ValueError:
            self.error.text = "Η ημερομηνία που διάλεξες δεν υπάρχει."
            return None

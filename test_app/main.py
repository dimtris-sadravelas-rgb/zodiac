from kivy.config import Config

Config.set("graphics", "width", "390")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", True)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from datetime import date


ZODIACS = [
    ("Αιγόκερως", "images/capricorn.png", "Ο Αιγόκερως είναι φιλόδοξος, πειθαρχημένος και σκέφτεται μακροπρόθεσμα.", (12, 22), (1, 19)),
    ("Υδροχόος", "images/aquarius.png", "Ο Υδροχόος είναι ανεξάρτητος, πρωτότυπος και σκέφτεται διαφορετικά.", (1, 20), (2, 18)),
    ("Ιχθύες", "images/pisces.png", "Οι Ιχθύες είναι ευαίσθητοι, ονειροπόλοι και έχουν έντονη φαντασία.", (2, 19), (3, 20)),
    ("Κριός", "images/aries.png", "Ο Κριός είναι δυναμικός, παρορμητικός και γεμάτος ενέργεια.", (3, 21), (4, 19)),
    ("Ταύρος", "images/taurus.png", "Ο Ταύρος αγαπά τη σταθερότητα, την άνεση και την ασφάλεια.", (4, 20), (5, 20)),
    ("Δίδυμοι", "images/gemini.png", "Οι Δίδυμοι είναι επικοινωνιακοί, περίεργοι και γρήγοροι στη σκέψη.", (5, 21), (6, 20)),
    ("Καρκίνος", "images/cancer.png", "Ο Καρκίνος είναι συναισθηματικός, προστατευτικός και δεμένος με την οικογένεια.", (6, 21), (7, 22)),
    ("Λέων", "images/leo.png", "Ο Λέων έχει αυτοπεποίθηση, δημιουργικότητα και έντονη παρουσία.", (7, 23), (8, 22)),
    ("Παρθένος", "images/virgo.png", "Η Παρθένος είναι οργανωτική, αναλυτική και προσέχει τις λεπτομέρειες.", (8, 23), (9, 22)),
    ("Ζυγός", "images/libra.png", "Ο Ζυγός αγαπά την ισορροπία, την αισθητική και τις καλές σχέσεις.", (9, 23), (10, 22)),
    ("Σκορπιός", "images/scorpio.png", "Ο Σκορπιός είναι έντονος, μυστηριώδης και βαθιά συναισθηματικός.", (10, 23), (11, 21)),
    ("Τοξότης", "images/sagittarius.png", "Ο Τοξότης αγαπά την ελευθερία, την περιπέτεια και τις νέες εμπειρίες.", (11, 22), (12, 21)),
]


def calculate_age(birth_date):
    today = date.today()

    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def find_zodiac(month, day):
    for name, image, text, start, end in ZODIACS:
        start_month, start_day = start
        end_month, end_day = end

        if start_month > end_month:
            if (month, day) >= start or (month, day) <= end:
                return name, image, text
        else:
            if start <= (month, day) <= end:
                return name, image, text

    return None


class BirthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=14
        )
        self.add_widget(self.layout)

        self.title = Label(
            text="Βρες το Ζώδιό σου",
            font_size=28,
            bold=True,
            size_hint_y=None,
            height=60
        )
        self.layout.add_widget(self.title)

        self.info = Label(
            text="Γράψε ημερομηνία γέννησης ή διάλεξέ την από τα πεδία.",
            font_size=17,
            size_hint_y=None,
            height=60
        )
        self.layout.add_widget(self.info)

        self.date_input = TextInput(
            hint_text="π.χ. 25/03/2000",
            multiline=False,
            font_size=22,
            size_hint_y=None,
            height=55
        )
        self.layout.add_widget(self.date_input)

        self.or_label = Label(
            text="ή επίλεξε με click",
            font_size=18,
            size_hint_y=None,
            height=35
        )
        self.layout.add_widget(self.or_label)

        self.spinner_row = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=None,
            height=55
        )
        self.layout.add_widget(self.spinner_row)

        self.day_spinner = Spinner(
            text="Ημέρα",
            values=[str(i) for i in range(1, 32)],
            font_size=18
        )

        self.month_spinner = Spinner(
            text="Μήνας",
            values=[str(i) for i in range(1, 13)],
            font_size=18
        )

        current_year = date.today().year

        self.year_spinner = Spinner(
            text="Χρονιά",
            values=[str(i) for i in range(current_year, 1900, -1)],
            font_size=18
        )

        self.spinner_row.add_widget(self.day_spinner)
        self.spinner_row.add_widget(self.month_spinner)
        self.spinner_row.add_widget(self.year_spinner)

        self.button = Button(
            text="Υπολόγισε",
            font_size=22,
            size_hint_y=None,
            height=60,
            background_color=(0.25, 0.35, 0.85, 1)
        )
        self.button.bind(on_press=self.calculate)
        self.layout.add_widget(self.button)

        self.error_label = Label(
            text="",
            font_size=17,
            color=(1, 0.2, 0.2, 1),
            size_hint_y=None,
            height=60
        )
        self.layout.add_widget(self.error_label)

    def calculate(self, instance):
        birth_date = None

        typed_date = self.date_input.text.strip()

        if typed_date != "":
            try:
                day, month, year = typed_date.split("/")
                birth_date = date(int(year), int(month), int(day))
            except:
                self.error_label.text = "Λάθος μορφή. Γράψε π.χ. 25/03/2000"
                return
        else:
            if (
                self.day_spinner.text == "Ημέρα"
                or self.month_spinner.text == "Μήνας"
                or self.year_spinner.text == "Χρονιά"
            ):
                self.error_label.text = "Πρέπει να συμπληρώσεις ημέρα, μήνα και χρονιά."
                return

            try:
                birth_date = date(
                    int(self.year_spinner.text),
                    int(self.month_spinner.text),
                    int(self.day_spinner.text)
                )
            except:
                self.error_label.text = "Η ημερομηνία που διάλεξες δεν υπάρχει."
                return

        if birth_date > date.today():
            self.error_label.text = "Η ημερομηνία γέννησης δεν μπορεί να είναι στο μέλλον."
            return

        age = calculate_age(birth_date)
        zodiac = find_zodiac(birth_date.month, birth_date.day)

        detail_screen = self.manager.get_screen("detail")
        detail_screen.show_result(age, zodiac)

        self.error_label.text = ""
        self.manager.current = "detail"


class ZodiacDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )
        self.add_widget(self.layout)

        self.title = Label(
            text="",
            font_size=30,
            bold=True,
            size_hint_y=None,
            height=60
        )
        self.layout.add_widget(self.title)

        self.age_label = Label(
            text="",
            font_size=22,
            size_hint_y=None,
            height=45
        )
        self.layout.add_widget(self.age_label)

        self.image = Image(
            source="",
            allow_stretch=True,
            keep_ratio=True,
            size_hint_y=0.5
        )
        self.layout.add_widget(self.image)

        self.description = Label(
            text="",
            font_size=20,
            halign="center",
            valign="top",
            text_size=(Window.width - 40, None),
            size_hint_y=0.3
        )
        self.layout.add_widget(self.description)

        self.back_button = Button(
            text="Πίσω",
            font_size=22,
            size_hint_y=None,
            height=60,
            background_color=(0.25, 0.35, 0.85, 1)
        )
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        Window.bind(on_resize=self.update_text_width)

    def show_result(self, age, zodiac):
        name, image, text = zodiac

        self.title.text = name
        self.age_label.text = f"Ηλικία: {age}"
        self.image.source = image
        self.description.text = text

    def update_text_width(self, *args):
        self.description.text_size = (Window.width - 40, None)

    def go_back(self, instance):
        self.manager.current = "birth"


class ZodiacApp(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(BirthScreen(name="birth"))
        manager.add_widget(ZodiacDetailScreen(name="detail"))
        return manager


ZodiacApp().run()
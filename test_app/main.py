from kivy.config import Config

Config.set("graphics", "width", "390")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", True)

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from datetime import date
import webbrowser


Window.softinput_mode = "resize"

store = JsonStore("user_data.json")


def get_font_extra():
    if store.exists("settings"):
        return store.get("settings").get("font_extra", 0)
    return 0


def set_font_extra(value):
    store.put("settings", font_extra=value)


def fs(size):
    scale = Window.width / 390
    return max(size, int(size * scale)) + get_font_extra()


def make_label(text, size=18, height=None, bold=False):
    label = Label(
        text=text,
        font_size=fs(size),
        bold=bold,
        halign="center",
        valign="top",
        text_size=(Window.width - 50, None),
        size_hint_y=None
    )

    if height is None:
        label.bind(
            texture_size=lambda instance, value:
            setattr(instance, "height", value[1] + 25)
        )
    else:
        label.height = height

    return label


ZODIACS = {
    "Κριός": {
        "image": "images/aries.png",
        "element": "Φωτιά",
        "color": "Κόκκινο",
        "number": "9",
        "text": "Ο Κριός είναι δυναμικός, άμεσος και γεμάτος ενέργεια. Θέλει δράση, πρωτοβουλία και δεν φοβάται τις νέες αρχές.",
        "strengths": "Θάρρος, αποφασιστικότητα, ενθουσιασμός.",
        "weaknesses": "Παρορμητικότητα, ανυπομονησία, νεύρα.",
        "daily": "Σήμερα είναι καλή μέρα για να πάρεις πρωτοβουλία, αλλά πρόσεχε να μη βιαστείς.",
        "compatible": ["Λέων", "Τοξότης", "Δίδυμοι"],
        "difficult": ["Καρκίνος", "Αιγόκερως", "Παρθένος"],
        "link": "https://www.zodiacsign.com/zodiac-signs/aries/"
    },
    "Ταύρος": {
        "image": "images/taurus.png",
        "element": "Γη",
        "color": "Πράσινο",
        "number": "6",
        "text": "Ο Ταύρος αγαπά τη σταθερότητα, την ασφάλεια και την άνεση. Είναι πρακτικός, υπομονετικός και επίμονος.",
        "strengths": "Σταθερότητα, υπομονή, αξιοπιστία.",
        "weaknesses": "Πείσμα, δυσκολία στην αλλαγή, κτητικότητα.",
        "daily": "Σήμερα ευνοείται η οργάνωση και η σταθερή προσπάθεια.",
        "compatible": ["Παρθένος", "Αιγόκερως", "Καρκίνος"],
        "difficult": ["Λέων", "Υδροχόος", "Τοξότης"],
        "link": "https://www.zodiacsign.com/zodiac-signs/taurus/"
    },
    "Δίδυμοι": {
        "image": "images/gemini.png",
        "element": "Αέρας",
        "color": "Κίτρινο",
        "number": "5",
        "text": "Οι Δίδυμοι είναι επικοινωνιακοί, έξυπνοι και περίεργοι. Τους αρέσει η πληροφορία, η αλλαγή και η συζήτηση.",
        "strengths": "Επικοινωνία, προσαρμοστικότητα, χιούμορ.",
        "weaknesses": "Αστάθεια, νευρικότητα, επιφανειακότητα.",
        "daily": "Σήμερα μια συζήτηση μπορεί να σου ανοίξει νέα οπτική.",
        "compatible": ["Ζυγός", "Υδροχόος", "Κριός"],
        "difficult": ["Παρθένος", "Ιχθύες", "Σκορπιός"],
        "link": "https://www.zodiacsign.com/zodiac-signs/gemini/"
    },
    "Καρκίνος": {
        "image": "images/cancer.png",
        "element": "Νερό",
        "color": "Ασημί",
        "number": "2",
        "text": "Ο Καρκίνος είναι συναισθηματικός, προστατευτικός και δεμένος με την οικογένεια. Έχει έντονη διαίσθηση.",
        "strengths": "Φροντίδα, ευαισθησία, αφοσίωση.",
        "weaknesses": "Κυκλοθυμία, υπερευαισθησία, άμυνα.",
        "daily": "Σήμερα δώσε σημασία στο ένστικτό σου, αλλά μην αφήσεις τον φόβο να σε κλείσει.",
        "compatible": ["Σκορπιός", "Ιχθύες", "Ταύρος"],
        "difficult": ["Κριός", "Ζυγός", "Υδροχόος"],
        "link": "https://www.zodiacsign.com/zodiac-signs/cancer/"
    },
    "Λέων": {
        "image": "images/leo.png",
        "element": "Φωτιά",
        "color": "Χρυσό",
        "number": "1",
        "text": "Ο Λέων είναι δημιουργικός, εκφραστικός και θέλει να ξεχωρίζει. Έχει γενναιοδωρία και έντονη παρουσία.",
        "strengths": "Αυτοπεποίθηση, δημιουργικότητα, ζεστασιά.",
        "weaknesses": "Εγωισμός, ανάγκη προσοχής, υπερβολή.",
        "daily": "Σήμερα μπορείς να λάμψεις, αρκεί να ακούσεις και τους άλλους.",
        "compatible": ["Κριός", "Τοξότης", "Ζυγός"],
        "difficult": ["Ταύρος", "Σκορπιός", "Αιγόκερως"],
        "link": "https://www.zodiacsign.com/zodiac-signs/leo/"
    },
    "Παρθένος": {
        "image": "images/virgo.png",
        "element": "Γη",
        "color": "Μπεζ",
        "number": "4",
        "text": "Η Παρθένος είναι αναλυτική, οργανωτική και πρακτική. Προσέχει τις λεπτομέρειες και θέλει βελτίωση.",
        "strengths": "Οργάνωση, λογική, υπευθυνότητα.",
        "weaknesses": "Υπερανάλυση, τελειομανία, αυστηρότητα.",
        "daily": "Σήμερα βάλε πρόγραμμα, αλλά μη χαθείς στις λεπτομέρειες.",
        "compatible": ["Ταύρος", "Αιγόκερως", "Καρκίνος"],
        "difficult": ["Δίδυμοι", "Τοξότης", "Κριός"],
        "link": "https://www.zodiacsign.com/zodiac-signs/virgo/"
    },
    "Ζυγός": {
        "image": "images/libra.png",
        "element": "Αέρας",
        "color": "Ροζ",
        "number": "7",
        "text": "Ο Ζυγός αγαπά την ισορροπία, την ομορφιά και τις σχέσεις. Θέλει αρμονία και δίκαιη συμπεριφορά.",
        "strengths": "Διπλωματία, γοητεία, κοινωνικότητα.",
        "weaknesses": "Αναποφασιστικότητα, εξάρτηση από γνώμες, αποφυγή σύγκρουσης.",
        "daily": "Σήμερα μια ήρεμη κουβέντα μπορεί να λύσει κάτι που σε πίεζε.",
        "compatible": ["Δίδυμοι", "Υδροχόος", "Λέων"],
        "difficult": ["Καρκίνος", "Αιγόκερως", "Ιχθύες"],
        "link": "https://www.zodiacsign.com/zodiac-signs/libra/"
    },
    "Σκορπιός": {
        "image": "images/scorpio.png",
        "element": "Νερό",
        "color": "Μαύρο",
        "number": "8",
        "text": "Ο Σκορπιός είναι έντονος, βαθύς και μυστηριώδης. Δεν μένει στην επιφάνεια και ζητά αλήθεια.",
        "strengths": "Πάθος, διαίσθηση, επιμονή.",
        "weaknesses": "Ζήλια, καχυποψία, έλεγχος.",
        "daily": "Σήμερα κράτα την ένταση δημιουργική και όχι καταστροφική.",
        "compatible": ["Καρκίνος", "Ιχθύες", "Αιγόκερως"],
        "difficult": ["Λέων", "Υδροχόος", "Δίδυμοι"],
        "link": "https://www.zodiacsign.com/zodiac-signs/scorpio/"
    },
    "Τοξότης": {
        "image": "images/sagittarius.png",
        "element": "Φωτιά",
        "color": "Μωβ",
        "number": "3",
        "text": "Ο Τοξότης αγαπά την ελευθερία, την περιπέτεια και τη γνώση. Θέλει να εξερευνά και να μαθαίνει.",
        "strengths": "Αισιοδοξία, ειλικρίνεια, περιπέτεια.",
        "weaknesses": "Απερισκεψία, υπερβολική ειλικρίνεια, ασυνέπεια.",
        "daily": "Σήμερα κράτα ανοιχτό μυαλό, αλλά μην αγνοήσεις τις υποχρεώσεις.",
        "compatible": ["Κριός", "Λέων", "Υδροχόος"],
        "difficult": ["Παρθένος", "Ιχθύες", "Ταύρος"],
        "link": "https://www.zodiacsign.com/zodiac-signs/sagittarius/"
    },
    "Αιγόκερως": {
        "image": "images/capricorn.png",
        "element": "Γη",
        "color": "Καφέ",
        "number": "10",
        "text": "Ο Αιγόκερως είναι φιλόδοξος, πειθαρχημένος και σοβαρός. Χτίζει αργά αλλά σταθερά.",
        "strengths": "Υπομονή, στόχος, αυτοέλεγχος.",
        "weaknesses": "Αυστηρότητα, απαισιοδοξία, εργασιομανία.",
        "daily": "Σήμερα ένα μικρό βήμα μπορεί να σε φέρει πιο κοντά σε μεγάλο στόχο.",
        "compatible": ["Ταύρος", "Παρθένος", "Σκορπιός"],
        "difficult": ["Κριός", "Ζυγός", "Λέων"],
        "link": "https://www.zodiacsign.com/zodiac-signs/capricorn/"
    },
    "Υδροχόος": {
        "image": "images/aquarius.png",
        "element": "Αέρας",
        "color": "Μπλε",
        "number": "11",
        "text": "Ο Υδροχόος είναι ανεξάρτητος, πρωτότυπος και διαφορετικός. Σκέφτεται έξω από τα συνηθισμένα.",
        "strengths": "Πρωτοτυπία, ελευθερία, ιδέες.",
        "weaknesses": "Απόσταση, πείσμα, απρόβλεπτη συμπεριφορά.",
        "daily": "Σήμερα μια νέα ιδέα μπορεί να σε ενθουσιάσει.",
        "compatible": ["Δίδυμοι", "Ζυγός", "Τοξότης"],
        "difficult": ["Ταύρος", "Σκορπιός", "Καρκίνος"],
        "link": "https://www.zodiacsign.com/zodiac-signs/aquarius/"
    },
    "Ιχθύες": {
        "image": "images/pisces.png",
        "element": "Νερό",
        "color": "Γαλάζιο",
        "number": "12",
        "text": "Οι Ιχθύες είναι ευαίσθητοι, ονειροπόλοι και δημιουργικοί. Έχουν φαντασία και έντονη ενσυναίσθηση.",
        "strengths": "Φαντασία, συμπόνια, διαίσθηση.",
        "weaknesses": "Ανασφάλεια, φυγή από την πραγματικότητα, σύγχυση.",
        "daily": "Σήμερα άκου το συναίσθημά σου, αλλά κράτα επαφή με την πραγματικότητα.",
        "compatible": ["Καρκίνος", "Σκορπιός", "Ταύρος"],
        "difficult": ["Δίδυμοι", "Τοξότης", "Ζυγός"],
        "link": "https://www.zodiacsign.com/zodiac-signs/pisces/"
    },
}


ZODIAC_DATES = [
    ("Αιγόκερως", (12, 22), (1, 19)),
    ("Υδροχόος", (1, 20), (2, 18)),
    ("Ιχθύες", (2, 19), (3, 20)),
    ("Κριός", (3, 21), (4, 19)),
    ("Ταύρος", (4, 20), (5, 20)),
    ("Δίδυμοι", (5, 21), (6, 20)),
    ("Καρκίνος", (6, 21), (7, 22)),
    ("Λέων", (7, 23), (8, 22)),
    ("Παρθένος", (8, 23), (9, 22)),
    ("Ζυγός", (9, 23), (10, 22)),
    ("Σκορπιός", (10, 23), (11, 21)),
    ("Τοξότης", (11, 22), (12, 21)),
]


def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def find_zodiac(month, day):
    for name, start, end in ZODIAC_DATES:
        if start[0] > end[0]:
            if (month, day) >= start or (month, day) <= end:
                return name
        else:
            if start <= (month, day) <= end:
                return name

    return None


class ConsentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = BoxLayout(orientation="vertical", padding=20, spacing=15)
        self.add_widget(main)

        main.add_widget(make_label("Αποδοχή Όρων", 30, height=65, bold=True))

        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)

        text = (
            "Πριν χρησιμοποιήσεις την εφαρμογή, πρέπει να αποδεχτείς την επεξεργασία "
            "των προσωπικών δεδομένων που εισάγεις.\n\n"
            "Η εφαρμογή μπορεί να ζητήσει όνομα, επίθετο, φύλο και ημερομηνία γέννησης. "
            "Τα δεδομένα χρησιμοποιούνται για να εμφανιστεί το ζώδιό σου, η ηλικία σου "
            "και προσωποποιημένες πληροφορίες.\n\n"
            "Σε αυτή την έκδοση τα δεδομένα αποθηκεύονται τοπικά στη συσκευή. "
            "Σε μελλοντική έκδοση μπορεί να σταλούν σε ασφαλή server μέσω HTTPS, "
            "μόνο αφού ενημερωθείς σχετικά.\n\n"
            "Τα ζώδια και οι προβλέψεις παρέχονται για ψυχαγωγικούς σκοπούς."
        )

        content.add_widget(make_label(text, 20))
        main.add_widget(scroll)

       self.accepted = False

 self.accept_button = Button(
    text="Δεν αποδέχτηκα τους όρους",
    font_size=fs(20),
    size_hint_y=None,
    height=65,
    background_color=(0.7, 0.2, 0.2, 1)
)

self.accept_button.bind(on_press=self.toggle_accept)

main.add_widget(self.accept_button)

        self.error = Label(
            text="",
            color=(1, 0.2, 0.2, 1),
            font_size=fs(18),
            size_hint_y=None,
            height=40
        )
        main.add_widget(self.error)

        button = Button(text="Συνέχεια", font_size=fs(24), size_hint_y=None, height=65)
        button.bind(on_press=self.accept)
        main.add_widget(button)

    def accept(self, instance):
        if not self.checkbox.active:
            self.error.text = "Πρέπει να αποδεχτείς τους όρους."
            return

        store.put("consent", accepted=True)
        self.manager.current = "profile"


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
            height=65
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
            height=65
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
            height=65
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

        link = Button(text="Άνοιγμα online ανάλυσης", font_size=fs(22), size_hint_y=None, height=65)
        link.bind(on_press=lambda instance: webbrowser.open(data["link"]))
        content.add_widget(link)

        edit = Button(text="Αλλαγή στοιχείων", font_size=fs(22), size_hint_y=None, height=65)
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


class CompatibilityScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        self.add_widget(self.layout)

    def show(self, my_sign, other_sign, is_good):
        self.layout.clear_widgets()

        self.layout.add_widget(make_label(f"{my_sign} με {other_sign}", 28, height=65, bold=True))

        if is_good:
            text = (
                f"Ο συνδυασμός {my_sign} και {other_sign} θεωρείται πιο συμβατός, γιατί τα δύο ζώδια "
                f"μπορούν να συμπληρώσουν το ένα το άλλο. Συνήθως υπάρχει καλύτερη ροή στην επικοινωνία, "
                f"περισσότερη κατανόηση και πιο εύκολο κοινό έδαφος.\n\n"
                f"Δεν σημαίνει ότι όλα είναι αυτόματα τέλεια. Σημαίνει ότι η σχέση ξεκινά με περισσότερες πιθανότητες συνεννόησης."
            )
        else:
            text = (
                f"Ο συνδυασμός {my_sign} και {other_sign} θεωρείται πιο δύσκολος, γιατί τα δύο ζώδια "
                f"μπορεί να έχουν διαφορετικές ανάγκες, ρυθμούς ή τρόπο έκφρασης.\n\n"
                f"Δεν σημαίνει ότι δεν μπορεί να πετύχει. Σημαίνει ότι χρειάζεται περισσότερη υπομονή, επικοινωνία και προσπάθεια."
            )

        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)

        content.add_widget(make_label(text, 22))

        self.layout.add_widget(scroll)

        back = Button(text="Πίσω", font_size=fs(24), size_hint_y=None, height=65)
        back.bind(on_press=lambda instance: setattr(self.manager, "current", "result"))
        self.layout.add_widget(back)


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

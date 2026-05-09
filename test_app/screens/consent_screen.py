from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label

from helpers import fs, make_label
from storage_manager import store


class ConsentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.accepted = False

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

        button = Button(
            text="Συνέχεια",
            font_size=fs(24),
            size_hint_y=None,
            height=65
        )
        button.bind(on_press=self.accept)
        main.add_widget(button)

    def toggle_accept(self, instance):
        self.accepted = not self.accepted

        if self.accepted:
            self.accept_button.text = "✓ Αποδέχτηκα τους όρους"
            self.accept_button.background_color = (0.2, 0.6, 0.25, 1)
        else:
            self.accept_button.text = "Δεν αποδέχτηκα τους όρους"
            self.accept_button.background_color = (0.7, 0.2, 0.2, 1)

    def accept(self, instance):
        if not self.accepted:
            self.error.text = "Πρέπει να αποδεχτείς τους όρους."
            return

        store.put("consent", accepted=True)
        self.manager.current = "profile"

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

from helpers import fs, make_label


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

        back = Button(
            text="Πίσω",
            font_size=fs(24),
            size_hint_y=None,
            height=65
        )
        back.bind(on_press=lambda instance: setattr(self.manager, "current", "result"))
        self.layout.add_widget(back)

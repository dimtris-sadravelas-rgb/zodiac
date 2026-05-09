
from datetime import date
from kivy.core.window import Window
from kivy.uix.label import Label

from storage_manager import get_font_extra
from zodiac_data import ZODIAC_DATES


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

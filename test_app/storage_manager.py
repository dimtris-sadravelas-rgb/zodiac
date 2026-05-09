
from kivy.storage.jsonstore import JsonStore

store = JsonStore("user_data.json")


def get_font_extra():
    if store.exists("settings"):
        return store.get("settings").get("font_extra", 0)
    return 0


def set_font_extra(value):
    store.put("settings", font_extra=value)

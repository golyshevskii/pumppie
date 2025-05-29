from enum import Enum


class Button(str, Enum):
    """Available buttons."""

    FAQ = "FAQ"
    CONFIRM = "Confirm"
    CANCEL = "Cancel"
    BACK = "Back"


btn = Button

from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QSpinBox


def get_value(widget):
    if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
        return widget.text()
    elif isinstance(widget, QComboBox):
        return widget.currentText()
    elif isinstance(widget, QSpinBox):
        return widget.value()
    return None


def get_placeholder(widget):
    if isinstance(widget, QLineEdit):
        return widget.placeholderText()
    return None


def set_value(widget, context, placeholder: str = "", combobox_item: list = []):
    if isinstance(widget, QLabel):
        if context:
            widget.setText(context)
    elif isinstance(widget, QLineEdit):
        if context:
            widget.setText(context)
        elif placeholder and placeholder != "":
            widget.setText("")
            widget.setPlaceholderText(placeholder)
    elif isinstance(widget, QComboBox):
        if context:
            widget.setCurrentText(context)
        if len(combobox_item) != 0:
            widget.addItems(combobox_item)
    elif isinstance(widget, QSpinBox):
        if context:
            widget.setValue(int(context))


def get_config(key):
    key_value_pairs = read_key_value_pairs()
    return key_value_pairs.get(key, "Key not found in the file.")


def read_key_value_pairs():
    key_value_pairs = {}
    with open("config//config.txt", "r", encoding = "utf-8") as file:
        for line in file:
            if line.strip().startswith("#"):
                continue
            key, value = line.strip().split(":")
            key_value_pairs[key] = value
    return key_value_pairs

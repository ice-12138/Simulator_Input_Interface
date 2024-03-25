from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QSpinBox
import os
import json


def getValue(widget):
    if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
        return widget.text()
    elif isinstance(widget, QComboBox):
        return widget.currentText()
    elif isinstance(widget, QSpinBox):
        return widget.value()
    return None


def setValue(widget, context):
    if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
        widget.setText(context)
    elif isinstance(widget, QComboBox):
        widget.setCurrentText(context)
    elif isinstance(widget, QSpinBox):
        widget.setValue(context)


def readJsonFile(fileName):
    dirPath = getConfig("json_path")
    file_path = os.path.join(dirPath, fileName + ".json")
    with open(file_path, "r") as file:
        data = json.load(file)
        print(data)


def getConfig(key):
    key_value_pairs = read_key_value_pairs()
    return key_value_pairs.get(key, "Key not found in the file.")


def read_key_value_pairs():
    key_value_pairs = {}
    with open("config//config.txt", "r", encoding="utf-8") as file:
        for line in file:
            if line.strip().startswith("#"):
                continue
            key, value = line.strip().split(":")
            key_value_pairs[key] = value
    return key_value_pairs

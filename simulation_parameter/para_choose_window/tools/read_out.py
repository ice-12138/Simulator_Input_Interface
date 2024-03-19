from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from enums.args import *
import re
import json
import os


def save_to_file(self, basic):
    file_name, _ = QFileDialog.getSaveFileName(
        self, "Save File", "", "Text Files (*.txt)"
    )
    if file_name:
        with open(file_name, "w") as file:
            file.write("{\n")
            for label, value in zip(basic.labels, basic.modules):
                if isinstance(value, QComboBox):
                    value = find_by_name(label, value.currentText())
                elif isinstance(value, QLineEdit):
                    value = find_by_name(label, value.text())
                elif isinstance(value, QSpinBox):
                    value = find_by_name(label, value.value())

                file.write(f"{label} = {value}\n")
            file.write("}\n")
    print("保存成功！")


def open_file(self, basic):
    file_path, _ = QFileDialog.getOpenFileName(
        self, "Open File", "", "Text Files (*.txt)"
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                pattern = r"(\w+)\s*=\s*(\w+)"
                matches = re.findall(pattern, content)

                values = []
                for match in matches:
                    values.append(find_by_value(match[0], match[1]))
                basic.updateValuesOpen(values)
        except Exception as e:
            print("无法打开文件")
            # waring_edit = QTextEdit(formLayoutWidget)
            # waring_edit.setPlainText("无法打开文件：{}".format(str(e)))


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

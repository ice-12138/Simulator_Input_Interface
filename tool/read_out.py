import logging

from PyQt5.QtWidgets import QFileDialog, QComboBox, QLineEdit, QSpinBox

from enums.args import *
import re
import json
import os
from tool import tool, mns_log

mns_log.mns_logging()


def save_to_file(self, basics):
    file_name, _ = QFileDialog.getSaveFileName(
        self, "Save File", "", "Text Files (*.txt)"
    )
    if file_name:
        with open(file_name, "w") as file:
            for basic in basics:
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


def open_file(self, basics):
    file_path, _ = QFileDialog.getOpenFileName(
        self, "Open File", "", "Text Files (*.txt)"
    )
    if file_path:
        try:
            with open(file_path, "r", encoding = "utf-8") as file:
                content = file.read()
                part = re.findall(r"\{([^}]*)\}", content)
                for i in range(len(part)):
                    pattern = r"(\w+)\s*=\s*(\w+)"
                    matches = re.findall(pattern, part[i])

                    values = []
                    for match in matches:
                        values.append(find_by_value(match[0], match[1]))
                    basics[i].update_values_open(values)
        except Exception as e:
            logging.warning("无法打开文件")
            # waring_edit = QTextEdit(formLayoutWidget)
            # waring_edit.setPlainText("无法打开文件：{}".format(str(e)))


def read_json_file(file_name):
    dir_path = tool.get_config("json_path")
    if ".json" not in file_name:
        file_path = os.path.join(dir_path, file_name + ".json")
    else:
        file_path = os.path.join(dir_path, file_name)
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except IOError:
        logging.error("未能找到该文件")
    return data

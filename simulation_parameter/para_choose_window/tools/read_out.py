from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from enums.args import *
import re


class ReadOut:
    @staticmethod
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
                        # value = value.text()
                        value = find_by_name(label, value.text())

                    elif isinstance(value, QSpinBox):
                        # value = value.value()
                        value = find_by_name(label, value.value())

                    file.write(f"{label} = {value}\n")
                file.write("}\n")
        print("保存成功！")

    @staticmethod
    def open_file(self, basic):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    # values = []
                    # # 使用正则表达式提取值
                    # pattern = r"=\s*(\S+)"
                    # matches = re.findall(pattern, content)
                    # values.extend(matches)
                    # basic.updateValuesOpen(values)
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

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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
                        value = value.currentText()
                    elif isinstance(value, QLineEdit):
                        value = value.text()
                    elif isinstance(value, QSpinBox):
                        value = value.value()
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
                    values = []
                    # 使用正则表达式提取值
                    pattern = r"=\s*(\S+)"
                    matches = re.findall(pattern, content)
                    values.extend(matches)
                    basic.updateValuesOpen(values)
            except Exception as e:
                print("无法打开文件")
                # waring_edit = QTextEdit(formLayoutWidget)
                # waring_edit.setPlainText("无法打开文件：{}".format(str(e)))

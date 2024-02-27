import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.lineEdit = QLineEdit(self)
        regex = QRegExp("[0-9]+")  # 正则表达式，表示只允许输入数字
        validator = QRegExpValidator(regex)
        self.lineEdit.setValidator(validator)

        layout.addWidget(self.lineEdit)

        self.setLayout(layout)

        self.setWindowTitle("只允许输入数字的 QLineEdit 示例")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

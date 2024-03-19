import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QVBoxLayout


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("警示窗示例")

        # 创建一个按钮用于弹出警告对话框
        self.warning_button = QPushButton("弹出警示窗")
        self.warning_button.clicked.connect(self.show_warning)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.warning_button)
        self.setLayout(layout)

    def show_warning(self):
        # 创建警告对话框
        warning = QMessageBox.warning(self, "警示", "确定要退出吗？", QMessageBox.Ok)

        # 如果用户点击了 Ok 按钮，则关闭警告窗口
        if warning == QMessageBox.Ok:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import sys

from simulation_parameter.para_choose_window import select_para_main
from simulation_parameter.edit_para_window import edit_para_main


class TitleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)  # 禁用标题栏和边框

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("E:\cover.jpg"))
        self.background_label.setGeometry(0, 0, 800, 450)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.showMainWindow)
        self.timer.start(5000)  # 设置5秒后显示主界面

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)  # 设置进度条范围
        self.progressBar.setValue(0)  # 初始值设为0
        self.progressBar.setGeometry(33, 375, 735, 20)
        self.progressBar.setStyleSheet("""  
            QProgressBar {  
                border: 2px solid grey;  
                border-radius: 5px;  
                text-align: center;  
                background-color: transparent;  
            }  
            QProgressBar::chunk {  
                background-color: #D3D3D3; /* 设置进度条的填充颜色 */  
            }  
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.progressBar)

        self.startProgress()

    def startProgress(self):
        # 创建一个定时器，每100毫秒更新一次进度条
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(100)

        # 假设进度条将在10秒内完成（10000毫秒），每次增加1
        self.max_value = 100
        self.current_value = 0

    def updateProgressBar(self):
        self.current_value += int(100 / 30)
        if self.current_value > 100:
            self.current_value = 100
        self.progressBar.setValue(self.current_value)

        # 当进度条到达最大值时，停止定时器
        if self.current_value >= self.max_value:
            self.timer.stop()

    def showMainWindow(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('主界面')
        self.resize(600, 400)

        # 创建一个菜单按钮
        menu_btn = QAction('菜单', self)
        menu_btn.triggered.connect(self.showMenu)

        # 创建一个菜单栏
        menubar = self.menuBar()
        menubar.addAction(menu_btn)

        self.show()

    def showMenu(self):
        # 创建一个下拉菜单
        menu = QMenu(self)
        option1 = menu.addAction('select parameters')
        option1.triggered.connect(self.option1Selected)

        # 在菜单按钮的位置显示下拉菜单
        menu.exec_(self.mapToGlobal(self.menuBar().pos()))

    def option1Selected(self):
        self.parameterWindow = select_para_main.MyApplication()
        self.parameterWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = TitleWindow()
    ui.show()
    sys.exit(app.exec_())


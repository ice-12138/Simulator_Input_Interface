from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from children_window.network_card import NetWork
import tools.read_out as ro
import sys
import os
import json


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("仿真参数选择")
        # 获取屏幕尺寸
        screen_size = QApplication.primaryScreen().size()
        width_percent = 0.4
        height_percent = 0.5
        window_width = screen_size.width() * width_percent
        window_height = screen_size.height() * height_percent
        self.resize(QSize(int(window_width), int(window_height)))
        # 参数列表选择
        self.menubar = QMenuBar(self)

        fileMenu = QMenu("&File", self)
        saveSubMenu = QAction("Save", self)
        saveSubMenu.triggered.connect(lambda: ro.save_to_file(self, basic))
        openSubMenu = QAction("Open", self)
        openSubMenu.triggered.connect(lambda: ro.open_file(self, basic))
        fileMenu.addAction(saveSubMenu)
        fileMenu.addAction(openSubMenu)
        self.menubar.addMenu(fileMenu)

        argMenu = QMenu("&Arg", self)
        # 获得参数列表文件夹下所有参数选择
        folderPath = ro.getConfig("json_path")
        names = os.listdir(folderPath)
        for name in names:
            if os.path.isfile(os.path.join(folderPath, name)):
                actionName = name.split(".")[0]
                subArgAction = QAction(actionName, self)
                subArgAction.triggered.connect(
                    lambda action, fileName=actionName: ro.readJsonFile(fileName)
                )
                argMenu.addAction(subArgAction)
        self.menubar.addMenu(argMenu)
        self.setMenuBar(self.menubar)

        # 创建主页面中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # 创建水平布局
        layout = QHBoxLayout()
        # 左侧
        self.left_widget = QListWidget(self)
        layout.addWidget(self.left_widget)

        self.left_widget.addItem("network")
        self.left_widget.addItem("router")
        self.left_widget.addItem("environment")

        self.left_widget.itemClicked.connect(self.on_btn_clicked)

        # 右侧
        right_widget = QWidget(self)
        right_layout = QVBoxLayout(right_widget)

        # 设置右侧堆载窗口
        self.right_up_widget = QStackedWidget()
        right_layout.addWidget(self.right_up_widget)

        # 网卡参数面板
        self.network_widget = QWidget()
        right_up_layout = NetWork()
        basic = right_up_layout.generate_window(self.network_widget)

        # 路由器参数面板
        self.router_widget = QWidget()
        lable2 = QLabel("路由器参数面板", self.router_widget)

        # 环境参数面板
        self.environment_widget = QWidget()
        lable3 = QLabel("环境参数面板", self.environment_widget)

        # 把参数面板加到堆载窗口中
        self.right_up_widget.addWidget(self.network_widget)
        self.right_up_widget.addWidget(self.router_widget)
        self.right_up_widget.addWidget(self.environment_widget)

        right_layout.addWidget(self.right_up_widget)

        layout.addWidget(right_widget)

        central_widget.setLayout(layout)

    def on_btn_clicked(self, item):
        device_name = item.text()
        if device_name == "network":
            self.right_up_widget.setCurrentIndex(0)
        elif device_name == "router":
            self.right_up_widget.setCurrentIndex(1)
        elif device_name == "environment":
            self.right_up_widget.setCurrentIndex(2)

    def addWidget(self, data):
        self.argsData = argsData


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyApplication()
    ui.show()
    sys.exit(app.exec_())

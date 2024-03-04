from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from children_window.network_card import NetWork
from tools import read_out as ro
import sys


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

        # 创建主页面中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # 创建水平布局
        layout = QHBoxLayout()
        # # 边缘比例
        # margin_percent = 0.02
        # # 竖边宽度
        # width_margin = margin_percent * window_width
        # # 横边宽度
        # height_margin = margin_percent * window_width
        # 左侧
        left_widget = QListWidget(self)
        layout.addWidget(left_widget)

        left_widget.addItem("network")
        left_widget.addItem("router")
        left_widget.addItem("environment")

        left_widget.itemClicked.connect(self.on_btn_clicked)

        # left_widget = QListWidget(self)
        # left_widget.addItem("network")
        # left_widget.addItem("router")
        # left_widget.addItem("environment")
        # layout.addWidget(left_widget)
        # 右侧
        right_widget = QWidget(self)
        right_layout = QVBoxLayout(right_widget)
        # 右上方
        # right_up_widget = QWidget(self)

        # right_up_layout = NetWork()
        # basic = right_up_layout.generate_window(right_up_widget)

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

        # # 右下方
        right_down_widget = QWidget(self)
        right_down_layout = QHBoxLayout(right_down_widget)

        save_button = QPushButton(right_down_widget)
        save_button.setText("save")
        save_button.clicked.connect(lambda: ro.ReadOut.save_to_file(self, basic))
        right_down_layout.addWidget(save_button)
        open_button = QPushButton(right_down_widget)
        open_button.setText("open")
        open_button.clicked.connect(lambda: ro.ReadOut.open_file(self, basic))
        right_down_layout.addWidget(open_button)
        cancel_button = QPushButton(right_down_widget)
        cancel_button.setText("cacel")
        cancel_button.clicked.connect(self.close)
        right_down_layout.addWidget(cancel_button)

        right_layout.addWidget(self.right_up_widget)
        right_layout.addWidget(right_down_widget)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyApplication()
    ui.show()
    sys.exit(app.exec_())

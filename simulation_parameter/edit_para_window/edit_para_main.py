from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from module.left_widget import *
from module.right_widget import *
import sys
import json


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        # 用于对应左边list和右边widget的关系
        self.assocArray = []
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("参数编辑")
        # 获取屏幕尺寸
        screen_size = QApplication.primaryScreen().size()
        width_percent = 0.5
        height_percent = 0.5
        window_width = screen_size.width() * width_percent
        window_height = screen_size.height() * height_percent
        self.resize(QSize(int(window_width), int(window_height)))
        # 菜单
        self.menubar = QMenuBar(self)
        fileMenu = QMenu("&File", self)
        saveSubMenu = QAction("Save", self)
        saveSubMenu.triggered.connect(lambda: self.saveJson())
        openSubMenu = QAction("Open", self)
        # openSubMenu.triggered.connect()
        fileMenu.addAction(saveSubMenu)
        fileMenu.addAction(openSubMenu)
        self.menubar.addMenu(fileMenu)
        self.setMenuBar(self.menubar)
        # 创建主页面中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # 创建水平布局
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        # 创建左侧列表
        leftWidget = SecListWidget(self)
        lw = leftWidget.setupUi()
        layout.addWidget(lw, 25)
        # 创建右侧窗口
        self.rw = QStackedWidget()
        self.addRightWidget()
        layout.addWidget(self.rw, 75)

    # 增加右侧堆叠框
    def addRightWidget(self):
        widget = SecTableWidget(self)
        self.rw.addWidget(widget.setupUi())
        self.assocArray.append(self.rw.count() - 1)

    # 变换右侧的显示项
    def changeWidget(self, index):
        self.rw.setCurrentIndex(index)

    # 删除右侧堆叠widget制定index的项
    def delWidget(self, index):
        widget = self.rw.widget(index)
        self.rw.removeWidget(widget)
        widget.deleteLater()

    def saveJson(self):
        dirPath = "jsonData"
        data = ""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", dirPath, "JSON Files (*.json)", options=options
        )
        if file_path:
            with open(file_path, "w") as json_file:
                json.dump(data, json_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())

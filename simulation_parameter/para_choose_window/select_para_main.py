from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from children_window.model import Model
import tools.read_out as ro
import tools.tool as tool
import sys
import os


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
        saveSubMenu.setShortcut("Ctrl+S")
        saveSubMenu.triggered.connect(lambda: self.save_to_file())
        openSubMenu = QAction("Open", self)
        openSubMenu.setShortcut("Ctrl+O")
        openSubMenu.triggered.connect(lambda: self.open_file())
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
                    lambda action, menu=argMenu, fileName=actionName: self.parsJson(
                        fileName
                    )
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
        layout.addWidget(self.left_widget, 30)
        self.left_widget.itemClicked.connect(self.on_btn_clicked)

        # 右侧
        right_widget = QWidget(self)
        right_layout = QVBoxLayout(right_widget)

        # 设置右侧堆载窗口
        self.right_up_widget = QStackedWidget()
        right_layout.addWidget(self.right_up_widget)

        layout.addWidget(right_widget, 70)

        central_widget.setLayout(layout)
        # 打开默认参数配置文件
        self.parsJson(tool.getConfig("default_args_file"))

    def on_btn_clicked(self, item):
        if isinstance(item, QListWidgetItemWithIndex):
            index = item.getIndex()
            self.right_up_widget.setCurrentIndex(index)

    # 读取并解析json文件生成界面
    def parsJson(self, fileName, action=None, menu=None):
        data = ro.readJsonFile(fileName)
        # 先删除目前有的list和widget
        self.left_widget.clear()
        while self.right_up_widget.count():
            widgetToRmove = self.right_up_widget.widget(0)
            self.right_up_widget.removeWidget(widgetToRmove)
            widgetToRmove.deleteLater()
        for key, value in data.items():
            self.addWidgte(key, value)

    def addWidgte(self, name, data):
        # 创建右边页面
        widget = QWidget()
        layout = Model()
        basic = layout.generate_window(widget, data)
        self.right_up_widget.addWidget(widget)
        count = self.left_widget.count()
        # 增加左侧list行数
        item = QListWidgetItemWithIndex(basic, count, name)
        self.left_widget.addItem(item)

    def save_to_file(self):
        ro.save_to_file(self, self.collectAllBasic())

    def open_file(self):
        ro.open_file(self, self.collectAllBasic())

    def collectAllBasic(self):
        basics = []
        # 遍历widget
        for i in range(self.left_widget.count()):
            item = self.left_widget.item(i)
            basics.append(item.getBasic())
        return basics

    def setCheckState(self, action, menu):
        # 设置被选中的action为checked，其他为unchecked
        for act in menu.actions():
            if act != action:
                act.setChecked(False)
            else:
                act.setChecked(True)


# list item中带有右侧widget的index
class QListWidgetItemWithIndex(QListWidgetItem):
    def __init__(self, basic, index: int, text: str, parent=None):
        super(QListWidgetItemWithIndex, self).__init__(parent)
        self.basic = basic
        self.index = index
        self.setText(text)
        self.currentText = text

    def getIndex(self):
        return self.index

    def setIndex(self, index):
        self.index = index

    def getBasic(self):
        return self.basic


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyApplication()
    ui.show()
    sys.exit(app.exec_())

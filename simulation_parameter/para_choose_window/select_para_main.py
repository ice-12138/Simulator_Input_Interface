from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenuBar, QMenu, QAction, QWidget, QHBoxLayout, QListWidget, \
    QVBoxLayout, QStackedWidget, QListWidgetItem

from simulation_parameter.para_choose_window.model import Model
from tool import tool, read_out
import sys
import os


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.right_up_widget = None
        self.menubar = None
        self.left_widget = None
        self.setup_ui()

    def setup_ui(self):
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

        file_menu = QMenu("&File", self)
        save_sub_menu = QAction("Save", self)
        save_sub_menu.setShortcut("Ctrl+S")
        save_sub_menu.triggered.connect(lambda: self.save_to_file())
        open_sub_menu = QAction("Open", self)
        open_sub_menu.setShortcut("Ctrl+O")
        open_sub_menu.triggered.connect(lambda: self.open_file())
        file_menu.addAction(save_sub_menu)
        file_menu.addAction(open_sub_menu)
        self.menubar.addMenu(file_menu)

        arg_menu = QMenu("&Arg", self)
        # 获得参数列表文件夹下所有参数选择
        folder_path = tool.get_config("json_path")
        names = os.listdir(folder_path)
        for name in names:
            if os.path.isfile(os.path.join(folder_path, name)):
                action_name = name.split(".")[0]
                sub_arg_action = QAction(action_name, self)
                sub_arg_action.triggered.connect(
                    lambda action, menu = arg_menu, file_name = action_name: self.pars_json(
                        file_name
                    )
                )
                arg_menu.addAction(sub_arg_action)
        self.menubar.addMenu(arg_menu)
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
        self.pars_json(tool.get_config("default_args_file"))

    def on_btn_clicked(self, item):
        if isinstance(item, QListWidgetItemWithIndex):
            index = item.get_index()
            self.right_up_widget.setCurrentIndex(index)

    # 读取并解析json文件生成界面
    def pars_json(self, file_name, action = None, menu = None):
        data = read_out.read_json_file(file_name)
        # 先删除目前有的list和widget
        self.left_widget.clear()
        while self.right_up_widget.count():
            widget_to_remove = self.right_up_widget.widget(0)
            self.right_up_widget.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
        for key, value in data.items():
            self.add_widget(key, value)

    def add_widget(self, name, data):
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
        read_out.save_to_file(self, self.collect_all_basic())

    def open_file(self):
        read_out.open_file(self, self.collect_all_basic())

    def collect_all_basic(self):
        basics = []
        # 遍历widget
        for i in range(self.left_widget.count()):
            item = self.left_widget.item(i)
            basics.append(item.get_basic())
        return basics

    def set_check_status(self, action, menu):
        # 设置被选中的action为checked，其他为unchecked
        for act in menu.actions():
            if act != action:
                act.setChecked(False)
            else:
                act.setChecked(True)


# list item中带有右侧widget的index
class QListWidgetItemWithIndex(QListWidgetItem):
    def __init__(self, basic, index: int, text: str, parent = None):
        super(QListWidgetItemWithIndex, self).__init__(parent)
        self.basic = basic
        self.index = index
        self.setText(text)
        self.currentText = text

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_basic(self):
        return self.basic


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyApplication()
    ui.show()
    sys.exit(app.exec_())

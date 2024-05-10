import logging

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenuBar, QMenu, QAction, QWidget, QHBoxLayout, QStackedWidget, \
    QFileDialog

from simulation_parameter.edit_para_window.module import left_widget, right_widget
import sys
import json

from simulation_parameter.edit_para_window.module.left_widget import SecListWidget
from simulation_parameter.edit_para_window.module.right_widget import SecTableWidget
from tool import tool, read_out, mns_log

mns_log.mns_logging()


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        # 用于对应左边list和右边widget的关系
        self.rw = None
        self.lw = None
        self.left_widget = None
        self.central_layout = None
        self.menubar = None
        self.table_widget = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("参数编辑")
        # 获取屏幕尺寸
        screen_size = QApplication.primaryScreen().size()
        width_percent = 0.6
        height_percent = 0.7
        window_width = screen_size.width() * width_percent
        window_height = screen_size.height() * height_percent
        self.resize(QSize(int(window_width), int(window_height)))
        # 菜单
        self.menubar = QMenuBar(self)
        file_menu = QMenu("&File", self)
        save_sub_menu = QAction("Save", self)
        save_sub_menu.setShortcut("Ctrl+S")
        save_sub_menu.triggered.connect(lambda: self.save_json())
        open_sub_menu = QAction("Open", self)
        open_sub_menu.setShortcut("Ctrl+O")
        open_sub_menu.triggered.connect(lambda: self.open_json())
        file_menu.addAction(save_sub_menu)
        file_menu.addAction(open_sub_menu)
        self.menubar.addMenu(file_menu)
        self.setMenuBar(self.menubar)
        # 创建主页面中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # 创建水平布局
        self.central_layout = QHBoxLayout()
        central_widget.setLayout(self.central_layout)
        # 创建左侧列表
        self.left_widget = SecListWidget(self)
        self.lw = self.left_widget.setup_ui()
        self.central_layout.addWidget(self.lw, 25)
        # 创建右侧窗口
        self.rw = QStackedWidget()
        self.add_right_widget()
        self.central_layout.addWidget(self.rw, 75)

    # 增加右侧堆叠框
    def add_right_widget(self):
        widget = SecTableWidget(self)
        self.rw.addWidget(widget.setup_ui())
        self.table_widget.append(widget)

    # 按所给数据增加右侧堆叠框

    # 变换右侧的显示项
    def change_widget(self, index):
        self.rw.setCurrentIndex(index)

    # 删除右侧堆叠widget制定index的项
    def delete_widget(self, index):
        widget = self.rw.widget(index)
        self.rw.removeWidget(widget)
        widget.deleteLater()

    def save_json(self):
        data = {}
        # 遍历所有左侧的list
        my_list = self.left_widget.get_list()
        for i in range(my_list.count()):
            item = my_list.item(i)
            # 右侧widget的index
            index = item.get_index()
            # 获得右侧界面的table
            table = self.rw.widget(index).layout().itemAt(0).widget()
            # 遍历table
            content = {}
            for row in range(table.rowCount()):
                row_value = []
                for col in range(table.columnCount()):
                    val = tool.get_value(table.cellWidget(row, col))
                    # 如果该列的参数名称为空，或碰到了第一个None值则继续进行下一行
                    if (col == 0 and val == "") or val is None:
                        break
                    row_value.append(val)
                if not row_value == []:
                    content.update({row: row_value})
            data.update({item.text(): content})
        dir_path = tool.get_config("json_path")
        options = QFileDialog.Options()
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", dir_path, "JSON Files (*.json)", options = options
            )
            if file_path:
                with open(file_path, "w") as json_file:
                    json.dump(data, json_file, indent = 4)
                    logging.info("文件保存成功！")
        except Exception:
            logging.warning("关闭文件打开窗口！")

    def open_json(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", tool.get_config("json_path"), "JSON Files (*.json)"
        )
        data = read_out.read_json_file(file_path)
        self.reset_all_widget(data)

    # 更新水平layout中的所有widget
    def reset_all_widget(self, data: dict):
        self.left_widget.setup_ui_by_exist(data)
        index = 0
        for value in data.values():
            self.add_right_widget_by_exist(value, index)
            index += 1
        # self.left_widget = SecListWidget(self)
        # lw = self.left_widget.setupUiByExist(data)
        # self.central_layout.addWidget(lw, 25)
        # self.rw = QStackedWidget()
        # self.central_layout.addWidget(self.rw, 75)

    def add_right_widget_by_exist(self, data, right_widget_index):
        if right_widget_index < len(self.table_widget):
            table_widget = self.table_widget[right_widget_index]
            if isinstance(table_widget, right_widget.SecTableWidget):
                # 删除原来的table
                table_widget.del_all()
                # 新建带有data的item
                table_widget.add_items(data)
        else:
            widget_class = right_widget.SecTableWidget(self)
            widget = widget_class.setup_ui_help()
            self.table_widget.append(widget)
            widget_class.add_items(data)
            self.rw.addWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QListWidgetItem
from tool import mns_log

mns_log.mns_logging()


class SecListWidget:
    def __init__(self, parent) -> None:
        self.del_button = None
        self.add_button = None
        self.list_widget = None
        self.parent = parent

    # 新建一个配置界面
    def setup_ui(self):
        widget = self.setup_ui_help()

        # 如果示例为空添加一个空白示例
        if self.list_widget.count() == 0:
            item = QListWidgetItemWithIndex(0)
            item.setText("untitled")
            self.list_widget.addItem(item)

        return widget

    # 打开保存的配置
    def setup_ui_by_exist(self, data: dict):
        # 如果item数量大于data的数量，删除多余item
        list_count = self.list_widget.count()
        if list_count > len(data):
            data_len = list_count - len(data)
            for i in range(data_len):
                self.list_widget.takeItem(list_count - 1 - i)
        index = 0
        # for key, value in data.items():
        #     self.add_item_by_exist(key, value, index)
        #     index += 1
        for key in data.keys():
            self.add_item_by_exist(key, index)
            index += 1

    def setup_ui_help(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(lambda item: self.change_right_widget(item))
        layout.addWidget(self.list_widget)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setDefaultDropAction(Qt.MoveAction)  # 设置默认的拖拽行为为移动

        # 设置双击可编辑
        self.list_widget.itemDoubleClicked.connect(lambda item: self.edit_item(item))

        # 创建添加和删除button
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.addStretch(1)

        # 新增button
        self.add_button = QPushButton("+")
        self.add_button.setFixedWidth(50)
        self.add_button.clicked.connect(lambda: self.add_item())
        button_layout.addWidget(self.add_button)
        # 删除button
        self.del_button = QPushButton("-")
        self.del_button.setFixedWidth(50)
        self.del_button.clicked.connect(lambda: self.del_item())
        button_layout.addWidget(self.del_button)

        layout.addWidget(button_widget)
        return widget

    # 编辑item
    def edit_item(self, item):
        # 如果不可编辑
        if not item.flags() & Qt.ItemIsEditable:
            # 设置为可编辑状态
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            # 编辑该项
            self.list_widget.editItem(item)

    # 新建item
    def add_item(self):
        # 父组件右侧重叠widget的数量
        count = self.parent.rw.count()
        # 增加左侧list行数
        item = QListWidgetItemWithIndex(count)
        self.list_widget.addItem(item)
        self.edit_item(item)
        # 对应增加右侧widget
        self.parent.add_right_widget()
        logging.info("左侧新增一行")

    # 从已存在的文件中读取配置
    def add_item_by_exist(self, name, index):
        if index < self.list_widget.count():  # 如果要修改的数量少于当前右边widget的数量
            # 修改左侧list的名字
            item = self.list_widget.item(index)
            item.setText(name)
        else:
            # 增加左侧list行数
            item = QListWidgetItemWithIndex(index, name)
            self.list_widget.addItem(item)
        # 对应增加右侧widget
        # self.parent.add_right_widget_by_exist(data, num_of_right)

    # 删除item
    def del_item(self):
        # 获得现在选择的item
        selected = self.list_widget.currentItem()
        if isinstance(selected, QListWidgetItemWithIndex):
            # 获得当前item所对应的右侧widget的index
            index = selected.get_index()
            # 删除当前item
            if selected:
                row = self.list_widget.row(selected)
                self.list_widget.takeItem(row)
            # 遍历所有item，将index位于当前index之后的index全部-1
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                if isinstance(item, QListWidgetItemWithIndex):
                    if item.get_index() > index:
                        item.set_index(item.get_index() - 1)
            # 删除对应右侧的widget
            self.parent.delete_widget(index)
            logging.info("左侧删除一行")

    # 变换右侧显示的widget
    def change_right_widget(self, item):
        self.parent.change_widget(item.get_index())

    def get_list(self):
        return self.list_widget


# list item中带有右侧widget的index
class QListWidgetItemWithIndex(QListWidgetItem):
    def __init__(self, index: int, text: str = "", parent = None):
        super(QListWidgetItemWithIndex, self).__init__(parent)
        self.index = index
        if not text == "":
            self.setText(text)

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

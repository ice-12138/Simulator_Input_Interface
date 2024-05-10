import logging

from PyQt5.QtWidgets import *
from tool import tool, mns_log

mns_log.mns_logging()


class SecTableWidget:
    def __init__(self, parent) -> None:
        self.add_button = None
        self.table_widget = None
        self.del_button = None
        self.parent = parent

    def setup_ui(self):
        widget = self.setup_ui_help()
        # 新建空白行
        if self.table_widget.rowCount() == 0:
            self.add_item()
        return widget

    def set_up_ui_by_exist(self, data):
        widget = self.setup_ui_help()

    def setup_ui_help(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        # 表格部分
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        horizontal_headers = [
            "para name",
            "alias",
            "unit",
            "input module",
            "input value",
            "input type",
            "del",
            "up",
            "down",
        ]
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(horizontal_headers)
        self.table_widget.setRowCount(0)

        # 创建添加和删除button
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.addStretch(1)

        # 新增button
        self.add_button = QPushButton("+")
        self.add_button.setFixedWidth(50)
        self.add_button.clicked.connect(lambda: self.add_item())
        button_layout.addWidget(self.add_button)

        layout.addWidget(button_widget)
        return widget

    def add_items(self, args):
        for i in range(len(args)):
            self.add_item(i, args[str(i)])

    # 新建item
    def add_item(self, row: int = 0, args: list = None):
        # 查看表格行数
        if not args:
            row = self.table_widget.rowCount()
        # 添加一行
        self.table_widget.insertRow(row)
        label = QLineEdit()
        tool.set_value(label, args[0] if args else "", "输入参数名称")
        self.table_widget.setCellWidget(row, 0, label)
        # 别名
        alias = QLineEdit()
        tool.set_value(alias, args[1] if args else "", "输入参数别名")
        self.table_widget.setCellWidget(row, 1, alias)
        # 单位
        unit_line = QLineEdit()
        tool.set_value(unit_line, args[2] if args else "", "','分割多个输入")
        self.table_widget.setCellWidget(row, 2, unit_line)
        # 输入部分
        input_box = QComboBox()
        tool.set_value(
            input_box,
            args[3] if args else "",
            combobox_item = ["line", "combox", "spinbox"],
        )
        self.table_widget.setCellWidget(row, 3, input_box)
        input_line = QLineEdit()
        tool.set_value(input_line, args[4] if args else "", "输入默认值")
        self.table_widget.setCellWidget(row, 4, input_line)
        input_type = QComboBox()
        tool.set_value(
            input_type, args[5] if args else "", combobox_item = ["all", "0-9", "a-zA-Z"]
        )
        self.table_widget.setCellWidget(row, 5, input_type)
        # 按钮

        del_button = QPushButton("-")
        del_button.setFixedWidth(20)
        del_button.setFixedHeight(20)
        up_button = QPushButton("↑")
        up_button.setFixedWidth(20)
        up_button.setFixedHeight(20)

        down_button = QPushButton("↓")
        down_button.setFixedWidth(20)
        down_button.setFixedHeight(20)

        del_button.clicked.connect(lambda: self.del_item())
        up_button.clicked.connect(lambda: self.up_item())
        down_button.clicked.connect(lambda: self.down_item())
        self.table_widget.setCellWidget(row, 6, del_button)
        self.table_widget.setCellWidget(row, 7, up_button)
        self.table_widget.setCellWidget(row, 8, down_button)
        self.table_widget.setColumnWidth(6, 40)
        self.table_widget.setColumnWidth(7, 40)
        self.table_widget.setColumnWidth(8, 40)
        # # 检查删除键是否可用
        # self.check_del_button_is_available()
        logging.info("新增输入行！")

    # 删除item
    def del_item(self):
        button = self.table_widget.sender()
        if button and self.table_widget.rowCount() > 1:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid():
                self.table_widget.removeRow(index.row())

    # 批量删除倒数n行
    def del_items(self, num):
        count = self.table_widget.rowCount()
        for i in range(num):
            self.table_widget.removeRow(count - i - 1)

    def del_all(self):
        self.del_items(self.table_widget.rowCount())

    # 向上移动item
    def up_item(self):
        button = self.table_widget.sender()
        if button:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid() and index.row() > 0:
                self.swap_rows(index.row(), index.row() - 1)

    # 向下移动item
    def down_item(self):
        button = self.table_widget.sender()
        if button and self.table_widget.rowCount() > 1:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid() and index.row() < self.table_widget.rowCount():
                self.swap_rows(index.row(), index.row() + 1)

    # 检查删除键是否可用（未使用）
    def check_del_button_is_available(self):
        if self.table_widget.rowCount() == 1:
            self.del_button.setEnabled(False)
        if self.table_widget.rowCount() > 1:
            self.del_button.setEnabled(True)

    # 交换两行的顺序
    def swap_rows(self, row1, row2):
        # 检查行号是否有效
        if (
                row1 < 0
                or row1 >= self.table_widget.rowCount()
                or row2 < 0
                or row2 >= self.table_widget.rowCount()
        ):
            return
        try:
            if row1 != row2:
                for col in range(self.table_widget.columnCount()):
                    # 获取第一行的窗口部件
                    text1 = tool.get_value(self.table_widget.cellWidget(row1, col))
                    place_holder1 = tool.get_placeholder(self.table_widget.cellWidget(row1, col))
                    # 获取第二行的窗口部件
                    text2 = tool.get_value(self.table_widget.cellWidget(row2, col))
                    place_holder2 = tool.get_placeholder(self.table_widget.cellWidget(row2, col))

                    # 将第一行和第二行的内容交换
                    if text1 or text2:
                        tool.set_value(self.table_widget.cellWidget(row1, col), text2, place_holder2)
                        tool.set_value(self.table_widget.cellWidget(row2, col), text1, place_holder1)
                logging.info("交换第" + str(row1) + "行与第" + str(row2) + "行成功！")
        except Exception:
            logging.debug("交换第" + str(row1) + "行与第" + str(row2) + "行失败！")

    def get_table(self):
        return self.table_widget

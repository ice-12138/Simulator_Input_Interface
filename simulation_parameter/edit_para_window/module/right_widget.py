from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SecTableWidget:
    def __init__(self, parent) -> None:
        self.parent = parent

    def setupUi(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        # 表格部分
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        horizontal_headers = [
            "para name",
            "unit",
            "unit value",
            "input type",
            "input value",
            "del",
            "up",
            "down",
        ]
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(horizontal_headers)
        self.table_widget.setRowCount(0)

        # 创建添加和删除button
        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout(buttonWidget)
        buttonLayout.addStretch(1)

        # 新增button
        self.addButton = QPushButton("+")
        self.addButton.setFixedWidth(50)
        self.addButton.clicked.connect(lambda: self.addItem())
        buttonLayout.addWidget(self.addButton)

        layout.addWidget(buttonWidget)
        # 如果示例为空添加一行
        if self.table_widget.rowCount() == 0:
            self.addItem()

        return widget

    # 新建item
    def addItem(self):
        # 查看表格行数
        row = self.table_widget.rowCount()
        # 添加一行
        self.table_widget.insertRow(row)
        label = QLineEdit()
        label.setPlaceholderText("输入参数名称")
        self.table_widget.setCellWidget(row, 0, label)
        # 单位部分
        unitBox = QComboBox()
        unitBox.addItems(["空", "下拉框"])
        self.table_widget.setCellWidget(row, 1, unitBox)
        unitLine = QLineEdit()
        unitLine.setPlaceholderText("','分割多个输入")
        self.table_widget.setCellWidget(row, 2, unitLine)
        # 输入部分
        inputBox = QComboBox()
        inputBox.addItems(["输入框", "下拉框", "数值选择"])
        self.table_widget.setCellWidget(row, 3, inputBox)
        inputLine = QLineEdit()
        inputLine.setPlaceholderText("输入默认值")
        self.table_widget.setCellWidget(row, 4, inputLine)
        # 按钮

        delButton = QPushButton("-")
        delButton.setFixedWidth(20)
        delButton.setFixedHeight(20)
        upButton = QPushButton("↑")
        upButton.setFixedWidth(20)
        upButton.setFixedHeight(20)

        downButton = QPushButton("↓")
        downButton.setFixedWidth(20)
        downButton.setFixedHeight(20)

        delButton.clicked.connect(lambda: self.delItem())
        upButton.clicked.connect(lambda: self.upItem())
        downButton.clicked.connect(lambda: self.downItem())
        self.table_widget.setCellWidget(row, 5, delButton)
        self.table_widget.setCellWidget(row, 6, upButton)
        self.table_widget.setCellWidget(row, 7, downButton)
        self.table_widget.setColumnWidth(5, 40)
        self.table_widget.setColumnWidth(6, 40)
        self.table_widget.setColumnWidth(7, 40)
        # # 检查删除键是否可用
        # self.checkDelButtonIsAvailable()

    # 删除item
    def delItem(self):
        button = self.table_widget.sender()
        if button and self.table_widget.rowCount() > 1:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid():
                self.table_widget.removeRow(index.row())

    # 向上移动item
    def upItem(self):
        button = self.table_widget.sender()
        if button:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid() and index.row() > 0:
                self.swapRows(index.row(), index.row() - 1)

    # 向下移动item
    def downItem(self):
        button = self.table_widget.sender()
        if button and self.table_widget.rowCount() > 1:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid() and index.row() < self.table_widget.rowCount():
                self.swapRows(index.row(), index.row() + 1)

    # 检查删除键是否可用（未使用）
    def checkDelButtonIsAvailable(self):
        if self.table_widget.rowCount() == 1:
            self.delButton.setEnabled(False)
        if self.table_widget.rowCount() > 1:
            self.delButton.setEnabled(True)

    # 交换两行的顺序
    def swapRows(self, row1, row2):
        # 检查行号是否有效
        if (
            row1 < 0
            or row1 >= self.table_widget.rowCount()
            or row2 < 0
            or row2 >= self.table_widget.rowCount()
        ):
            return
        if row1 != row2:
            for col in range(self.table_widget.columnCount()):
                # 获取第一行的窗口部件
                text1 = self.getValue(self.table_widget.cellWidget(row1, col))
                # 获取第二行的窗口部件
                text2 = self.getValue(self.table_widget.cellWidget(row2, col))
                # 将第一行和第二行的内容交换
                if text1 or text2:
                    self.setValue(self.table_widget.cellWidget(row1, col), text2)
                    self.setValue(self.table_widget.cellWidget(row2, col), text1)

    def getValue(self, widget):
        if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QComboBox):
            return widget.currentText()
        return None

    def setValue(self, widget, context):
        if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
            widget.setText(context)
        elif isinstance(widget, QComboBox):
            widget.setCurrentText(context)

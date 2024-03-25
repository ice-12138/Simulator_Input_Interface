from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import module.tools.tool as tool


class SecTableWidget:
    def __init__(self, parent) -> None:
        self.parent = parent

    def setupUi(self):
        widget = self.setupUiHelp()
        # 新建空白行
        if self.table_widget.rowCount() == 0:
            self.addItem()
        return widget

    def setupUiByExist(self, data):
        widget = self.setupUiHelp()

    def setupUiHelp(self):
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
        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout(buttonWidget)
        buttonLayout.addStretch(1)

        # 新增button
        self.addButton = QPushButton("+")
        self.addButton.setFixedWidth(50)
        self.addButton.clicked.connect(lambda: self.addItem())
        buttonLayout.addWidget(self.addButton)

        layout.addWidget(buttonWidget)
        return widget

    def addItems(self, args):
        for i in range(len(args)):
            self.addItem(args[str(i)])

    # 新建item
    def addItem(self, args: list = []):
        # 查看表格行数
        row = self.table_widget.rowCount()
        # 添加一行
        self.table_widget.insertRow(row)
        label = QLineEdit()
        if len(args) == 0 or (args[0] and args[0] == ""):
            label.setPlaceholderText("输入参数名称")
        else:
            tool.setValue(label, args[0])
        self.table_widget.setCellWidget(row, 0, label)
        # 别名
        alias = QLineEdit()
        if len(args) == 0 or (args[1] and args[1] == ""):
            alias.setPlaceholderText("输入参数别名")
        else:
            tool.setValue(alias, args[1])
        self.table_widget.setCellWidget(row, 1, alias)
        # 单位
        unitLine = QLineEdit()
        if len(args) == 0 or (args[2] and args[2] == ""):
            unitLine.setPlaceholderText("','分割多个输入")
        else:
            tool.setValue(unitLine, args[2])
        self.table_widget.setCellWidget(row, 2, unitLine)
        # 输入部分
        inputBox = QComboBox()
        inputBox.addItems(["line", "combox", "spinbox"])
        if not (len(args) == 0 or (args[3] and args[3] == "")):
            tool.setValue(inputBox, args[3])
        self.table_widget.setCellWidget(row, 3, inputBox)
        inputLine = QLineEdit()
        if len(args) == 0 or (args[4] and args[4] == ""):
            inputLine.setPlaceholderText("输入默认值")
        else:
            tool.setValue(inputLine, args[4])
        self.table_widget.setCellWidget(row, 4, inputLine)
        inputType = QComboBox()
        inputType.addItems(["all", "0-9", "a-zA-Z"])
        if not (len(args) == 0 or (args[5] and args[5] == "")):
            tool.setValue(inputType, args[5])
        self.table_widget.setCellWidget(row, 5, inputType)
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
        self.table_widget.setCellWidget(row, 6, delButton)
        self.table_widget.setCellWidget(row, 7, upButton)
        self.table_widget.setCellWidget(row, 8, downButton)
        self.table_widget.setColumnWidth(6, 40)
        self.table_widget.setColumnWidth(7, 40)
        self.table_widget.setColumnWidth(8, 40)
        # # 检查删除键是否可用
        # self.checkDelButtonIsAvailable()

    # 删除item
    def delItem(self):
        button = self.table_widget.sender()
        if button and self.table_widget.rowCount() > 1:
            index = self.table_widget.indexAt(button.pos())
            if index.isValid():
                self.table_widget.removeRow(index.row())

    # 批量删除倒数n行
    def delItems(self, num):
        count = self.table_widget.rowCount()
        for i in range(num):
            self.table_widget.removeRow(count - i - 1)

    def delAll(self):
        self.delItems(self.table_widget.rowCount())

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
                text1 = tool.getValue(self.table_widget.cellWidget(row1, col))
                # 获取第二行的窗口部件
                text2 = tool.getValue(self.table_widget.cellWidget(row2, col))
                # 将第一行和第二行的内容交换
                if text1 or text2:
                    tool.setValue(self.table_widget.cellWidget(row1, col), text2)
                    tool.setValue(self.table_widget.cellWidget(row2, col), text1)

    def getTable(self):
        return self.table_widget

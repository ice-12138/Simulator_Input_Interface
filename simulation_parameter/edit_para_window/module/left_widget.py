from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import singledispatch


class SecListWidget:
    def __init__(self, parent) -> None:
        self.parent = parent

    # 新建一个配置界面
    def setupUi(self):
        widget = self.setupUiHelp()

        # 如果示例为空添加一个空白示例
        if self.listWidget.count() == 0:
            item = QListWidgetItemWithIndex(0)
            item.setText("untitled")
            self.listWidget.addItem(item)

        return widget

    # 打开保存的配置
    def setupUiByExist(self, data: dict):
        # 如果item数量大于data的数量，删除多余item
        listCount = self.listWidget.count()
        if listCount > len(data):
            datalen = listCount - len(data)
            for i in range(datalen):
                self.listWidget.takeItem(listCount - 1 - i)
        index = 0
        for key, value in data.items():
            self.addItemByExist(key, value, index)
            index += 1

    def setupUiHelp(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(lambda item: self.changeRightWidget(item))
        layout.addWidget(self.listWidget)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)  # 设置默认的拖拽行为为移动

        # 设置双击可编辑
        self.listWidget.itemDoubleClicked.connect(lambda item: self.edit_item(item))

        # 创建添加和删除button
        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout(buttonWidget)
        buttonLayout.addStretch(1)

        # 新增button
        self.addButton = QPushButton("+")
        self.addButton.setFixedWidth(50)
        self.addButton.clicked.connect(lambda: self.add_item())
        buttonLayout.addWidget(self.addButton)
        # 删除button
        self.delButton = QPushButton("-")
        self.delButton.setFixedWidth(50)
        self.delButton.clicked.connect(lambda: self.del_item())
        buttonLayout.addWidget(self.delButton)

        layout.addWidget(buttonWidget)
        return widget

    # 编辑item
    def edit_item(self, item):
        # 如果不可编辑
        if not item.flags() & Qt.ItemIsEditable:
            # 设置为可编辑状态
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            # 编辑该项
            self.listWidget.editItem(item)

    # 新建item
    def add_item(self):
        # 父组件右侧重叠widget的数量
        count = self.parent.rw.count()
        # 增加左侧list行数
        item = QListWidgetItemWithIndex(count)
        self.listWidget.addItem(item)
        self.edit_item(item)
        # 对应增加右侧widget
        self.parent.addRightWidget()

    # 从已存在的文件中读取配置
    # numOfRight:修改右面第几个widget
    def addItemByExist(self, name, data, numOfRight):
        # 父组件右侧重叠widget的数量
        count = self.parent.rw.count()
        if numOfRight <= count:  # 如果要修改的数量少于当前右边widget的数量
            # 修改左侧list的名字
            item = self.listWidget.item(numOfRight)
            item.setText(name)
        else:
            # 增加左侧list行数
            item = QListWidgetItemWithIndex(numOfRight, name)
            self.listWidget.addItem(item)
        # 对应增加右侧widget
        self.parent.addRightWidgetByExist(data, numOfRight)

    # 删除item
    def del_item(self):
        # 获得现在选择的item
        selected = self.listWidget.currentItem()
        # 获得当前item所对应的右侧widget的index
        index = selected.getIndex()
        # 删除当前item
        if selected is not None:
            row = self.listWidget.row(selected)
            self.listWidget.takeItem(row)
        # 遍历所有item，将index位于当前index之后的index全部-1
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.getIndex() > index:
                item.setIndex(item.getIndex() - 1)
        # 删除对应右侧的widget
        self.parent.delWidget(index)

    # 变换右侧显示的widget
    def changeRightWidget(self, item):
        self.parent.changeWidget(item.getIndex())

    def getList(self):
        return self.listWidget


# list item中带有右侧widget的index
class QListWidgetItemWithIndex(QListWidgetItem):
    def __init__(self, index: int, text: str = "", parent=None):
        super(QListWidgetItemWithIndex, self).__init__(parent)
        self.index = index
        if not text == "":
            self.setText(text)

    def getIndex(self):
        return self.index

    def setIndex(self, index):
        self.index = index

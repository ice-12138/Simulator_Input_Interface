from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SecListWidget:
    def __init__(self, parent) -> None:
        self.parent = parent

    def setupUi(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(lambda item: self.changeRightWidget(item))
        layout.addWidget(self.listWidget)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)  # 设置默认的拖拽行为为移动

        # 如果示例为空添加一个空白示例
        if self.listWidget.count() == 0:
            item = QListWidgetItemWithIndex(0)
            item.setText("untitled")
            self.listWidget.addItem(item)

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


# list item中带有右侧widget的index
class QListWidgetItemWithIndex(QListWidgetItem):
    def __init__(self, index: int, parent=None):
        super(QListWidgetItemWithIndex, self).__init__(parent)
        self.index = index

    def getIndex(self):
        return self.index

    def setIndex(self, index):
        self.index = index

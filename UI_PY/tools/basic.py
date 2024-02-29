from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from enums.module_type import *
from enums.input_type import *

# round:该组件在哪个范围
# parent：该组件的父布局
# alias:输出到txt中的名字
# text：该组件的内容
# module_type：该组件类型
# output:该组件的内容是否要输出到txt
# row：该组件位于父布局的第几行


class Basic:
    def __init__(self, mainWindow, arguments):
        self.mainWindow = mainWindow
        self.parent = QFormLayout(mainWindow)
        self.row = -1
        self.arguments = arguments
        self.labels = []
        self.modules = []
        self.leader = ""

    def create(
        self,
        module_type,
        text: str,
        output: bool = False,
        leader: bool = False,
        name: str = "",
        input_type: InputType = "",
    ):

        if module_type == Module.LABEL:
            # 每个label标签换行
            self.row += 1
            self.module_type = QLabel(self.mainWindow)
            self.module_type.setText(text)
            if isinstance(self.parent, QFormLayout):
                self.parent.setWidget(self.row, QFormLayout.LabelRole, self.module_type)
            if name != "":
                self.labels.append(name)

        if module_type == Module.COMBOX:
            self.module_type = QComboBox(self.mainWindow)
            self.module_type.addItems(text)
            if isinstance(self.parent, QFormLayout):
                self.parent.setWidget(self.row, QFormLayout.FieldRole, self.module_type)
            if output:
                self.modules.append(self.module_type)
            # 如果该选项会影响后面的value
            if leader:
                self.leader = self.module_type

        if module_type == Module.LINEEDIT:
            self.module_type = QLineEdit(self.mainWindow)
            self.module_type.setText(text)
            if isinstance(self.parent, QFormLayout):
                self.parent.setWidget(self.row, QFormLayout.FieldRole, self.module_type)
            if output:
                self.modules.append(self.module_type)

        if module_type == Module.SPINBOX:
            self.module_type = QSpinBox(self.mainWindow)
            self.module_type.setValue(text)
            if isinstance(self.parent, QFormLayout):
                self.parent.setWidget(self.row, QFormLayout.FieldRole, self.module_type)
            if output:
                self.modules.append(self.module_type)

        self.inputTypeCheck(input_type, self.module_type)

        return self.module_type

    def createLayout(self, module_type, child):
        if module_type == Layout.HBOX:
            self.layout = QHBoxLayout()
            for i in child:
                self.layout.addWidget(i)
            if isinstance(self.parent, QFormLayout):
                self.parent.setLayout(self.row, QFormLayout.FieldRole, self.layout)

    def createChild(
        self, module_type, text: str, output: bool = False, input_type: InputType = ""
    ):
        if module_type == Module.COMBOX:
            self.module_type = QComboBox(self.mainWindow)
            self.module_type.addItems(text)
            if output:
                self.modules.append(self.module_type)

        if module_type == Module.LINEEDIT:
            self.module_type = QLineEdit(self.mainWindow)
            self.module_type.setText(text)
            if output:
                self.modules.append(self.module_type)

        self.inputTypeCheck(input_type, self.module_type)

        return self.module_type

    def updateValues(self, index):
        argument = self.arguments[index]
        for i in range(len(self.modules)):
            if isinstance(self.modules[i], QComboBox):
                self.modules[i].setCurrentText(argument[i + 1])

            if isinstance(self.modules[i], QLineEdit):
                self.modules[i].setText(argument[i + 1])

            if isinstance(self.modules[i], QSpinBox):
                self.modules[i].setValue(int(argument[i + 1]))

    def updateValuesOpen(self, values):
        for i in range(len(self.modules)):
            if isinstance(self.modules[i], QComboBox):
                self.modules[i].setCurrentText(values[i])
            if isinstance(self.modules[i], QLineEdit):
                self.modules[i].setText(values[i])

            if isinstance(self.modules[i], QSpinBox):
                self.modules[i].setValue(int(values[i]))

    # def show_warning(self, waring_context):
    #     # 创建警告对话框
    #     warning = QMessageBox.warning(
    #         self.parent, "警示", waring_context, QMessageBox.Ok
    #     )

    #     # 如果用户点击了 Ok 按钮，则关闭警告窗口
    #     if warning == QMessageBox.Ok:
    #         warning.close()
    def inputTypeCheck(self, input_type, model):
        if input_type == InputType.ALPHA:
            regex = QRegExp("[a-zA-Z]+")
            validator = QRegExpValidator(regex)
            model.setValidator(validator)

        if input_type == InputType.DIGIT:
            regex = QRegExp("[0-9]+")
            validator = QRegExpValidator(regex)
            model.setValidator(validator)

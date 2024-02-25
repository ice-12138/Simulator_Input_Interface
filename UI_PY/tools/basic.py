from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
import typing
# round:该组件在哪个范围
# parent：该组件的父布局
# alias:输出到txt中的名字
# text：该组件的内容
# module_type：该组件类型
# output:该组件的内容是否要输出到txt
# row：该组件位于父布局的第几行


class basic():
    def __init__(self, mainWindow,  arguments):
        self.mainWindow = mainWindow
        self.parent = QtWidgets.QFormLayout(mainWindow)
        self.row = -1
        self.arguments = arguments
        self.labels = []
        self.modules = []
        self.leader = ""

    def create(self, module_type, text: str, output: bool = False, leader: bool = False, name: str = ""):

        if module_type == "label":
            # 每个label标签换行
            self.row += 1
            self.module_type = QtWidgets.QLabel(self.mainWindow)
            self.module_type.setText(text)
            if isinstance(self.parent, QtWidgets. QFormLayout):
                self.parent.setWidget(
                    self.row, QtWidgets.QFormLayout.LabelRole, self.module_type)
            if name != "":
                self.labels.append(name)

        if module_type == "combox":
            self.module_type = QtWidgets.QComboBox(self.mainWindow)
            self.module_type.addItems(text)
            if isinstance(self.parent, QtWidgets. QFormLayout):
                self.parent.setWidget(
                    self.row, QtWidgets.QFormLayout.FieldRole, self.module_type)
            if output:
                self.modules.append(self.module_type)
            # 如果该选项会影响后面的value
            if leader:
                # self.module_type.currentIndexChanged.connect(self.updateValues)
                # print(self.module_type.currentText())
                self.leader = self.module_type

        if module_type == "line":
            self.module_type = QtWidgets.QLineEdit(self.mainWindow)
            self.module_type.setText(text)
            if isinstance(self.parent, QtWidgets.QFormLayout):
                self.parent.setWidget(
                    self.row, QtWidgets.QFormLayout.FieldRole, self.module_type)
            if output:
                self.modules.append(self.module_type)

        if module_type == "spinbox":
            self.module_type = QtWidgets.QSpinBox(self.mainWindow)
            self.module_type.setValue(text)
            if isinstance(self.parent, QtWidgets.QFormLayout):
                self.parent.setWidget(
                    self.row, QtWidgets.QFormLayout.FieldRole, self.module_type)
            if output:
                self.modules.append(self.module_type)

        return self.module_type
    
    def createLayout(self, module_type, child):
        if module_type == "hbox":
            self.layout = QtWidgets.QHBoxLayout()
            for i in child:
                self.layout.addWidget(i)
            if isinstance(self.parent, QtWidgets.QFormLayout):
                self.parent.setLayout(
                    self.row, QtWidgets.QFormLayout.FieldRole, self.layout)

    def createChild(self, module_type, text: str, output: bool = False):

        if module_type == "combox":
            self.module_type = QtWidgets.QComboBox(self.mainWindow)
            self.module_type.addItems(text)
            if output:
                self.modules.append(self.module_type)

        if module_type == "line":
            self.module_type = QtWidgets.QLineEdit(self.mainWindow)
            self.module_type.setText(text)
            if output:
                self.modules.append(self.module_type)

        return self.module_type
    
    def updateValues(self, index):
        argument = self.arguments[index]
        for i in range(len(self.modules)):
            if isinstance(self.modules[i],QtWidgets.QComboBox):
                self.modules[i].setCurrentText(argument[i+1])
                
            if isinstance(self.modules[i],QtWidgets.QLineEdit):
                self.modules[i].setText(argument[i+1])

            if isinstance(self.modules[i],QtWidgets.QSpinBox):
                self.modules[i].setValue(int(argument[i+1]))


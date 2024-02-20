from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
# round:该组件在哪个范围
# parent：该组件的父布局
# alias:输出到txt中的名字
# text：该组件的内容
# module_type：该组件类型
# output:该组件的内容是否要输出到txt
# row：该组件位于父布局的第几行


class basic():
    def __init__(self, mainWindow,parent):
        self.mainWindow = mainWindow
        self.parent = parent
        self.row = -1
        self.labels = []
        self.values = []

    def create(self, module_type, text: str, output: bool = False, name: str = ""):    

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
                self.values.append(self.module_type.currentText())

        if module_type == "line":
            self.module_type = QtWidgets.QLineEdit(self.mainWindow)
            self.module_type.setText(text)
            if isinstance(self.parent,QtWidgets.QFormLayout):
                self.parent.setWidget(self.row, QtWidgets.QFormLayout.FieldRole, self.module_type)
            if output:
                self.values.append(self.module_type.text())

        if module_type == "spinbox":
            self.module_type = QtWidgets.QSpinBox(self.mainWindow)
            self.module_type.setValue(text)
            if isinstance(self.parent,QtWidgets.QFormLayout):
                self.parent.setWidget(self.row, QtWidgets.QFormLayout.FieldRole, self.module_type)
            if output:
                self.values.append(self.module_type.value())

        return self.module_type
    
    def createChild(self, module_type, text: str, output: bool = False):
        
        if module_type == "combox":
            self.module_type = QtWidgets.QComboBox(self.mainWindow)
            self.module_type.addItems(text)
            if output:
                self.values.append(self.module_type.currentText())

        if module_type == "line":
            self.module_type = QtWidgets.QLineEdit(self.mainWindow)
            self.module_type.setText(text)
            if output:
                self.values.append(self.module_type.text())

        return self.module_type
        
    def createLayout(self,module_type,child):
        if module_type == "hbox":
            self.layout = QtWidgets.QHBoxLayout()
            for i in child:
                self.layout.addWidget(i)
            if isinstance(self.parent,QtWidgets.QFormLayout):
                self.parent.setLayout(self.row, QtWidgets.QFormLayout.FieldRole, self.layout)
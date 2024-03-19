from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QSpinBox


def getValue(widget):
    if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
        return widget.text()
    elif isinstance(widget, QComboBox):
        return widget.currentText()
    elif isinstance(widget, QSpinBox):
        return widget.value()
    return None


def setValue(widget, context):
    if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
        widget.setText(context)
    elif isinstance(widget, QComboBox):
        widget.setCurrentText(context)
    elif isinstance(widget, QSpinBox):
        widget.setValue(context)

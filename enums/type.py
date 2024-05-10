from enum import Enum


class InputType(Enum):
    ALNUM = 1
    ALPHA = 2
    DIGIT = 3


class ModuleType(Enum):
    COMBOX = "combox"
    LINEEDIT = "lineedit"
    LABEL = "label"

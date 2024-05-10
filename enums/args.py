# 用于存放输入输出时参数名称对应的数字
from enum import Enum


class Antid(Enum):
    SISO = 0
    MIMO = 1
    directional = 2
    omni = 3

    def to_array(self):
        array = []
        for item in Antid:
            array.append(item.name)
        return array

    def get_value(name):
        for item in Antid:
            if item.name == name:
                return item.value

    def get_name(value):
        for item in Antid:
            if item.value == value:
                return item.name


class Mtype(Enum):
    radio = 0
    laser = 1
    acoustic = 2
    fiber = 3

    def array(self):
        array = []
        for item in Mtype:
            array.append(item.name)
        return array

    def get_value(name):
        for item in Mtype:
            if item.name == name:
                return item.value

    def get_name(value):
        for item in Mtype:
            if item.value == value:
                return item.name


class Cmode(Enum):
    duple = 0
    simplex = 1

    def array(self):
        array = []
        for item in Cmode:
            array.append(item.name)
        return array

    def get_value(name):
        for item in Cmode:
            if item.name == name:
                return item.value

    def get_name(value):
        for item in Cmode:
            if item.value == value:
                return item.name


def find_by_name(clas: str, name):
    if clas == "antid":
        return Antid.get_value(name)
    elif clas == "mtype":
        return Mtype.get_value(name)
    elif clas == "cmode":
        return Cmode.get_value(name)
    else:
        return name


def find_by_value(clas: str, value):
    if clas == "antid":
        return Antid.get_name(value)
    elif clas == "mtype":
        return Mtype.get_name(value)
    elif clas == "cmode":
        return Cmode.get_name(value)
    else:
        return value

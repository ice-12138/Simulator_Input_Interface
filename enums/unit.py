from enum import Enum


class FrequencyUnit(Enum):
    HZ = "Hz"
    MHZ = "MHz"
    GHZ = "GHz"

    def to_array(self):
        array = []
        for item in FrequencyUnit:
            array.append(item.value)
        return array


class SpeedUnit(Enum):
    BITSS = "bits/s"
    MBITSS = "Mbits/s"
    GBITSS = "Gbits/s"

    def to_array(self):
        array = []
        for item in SpeedUnit:
            array.append(item.value)
        return array


class DistanceUnit(Enum):
    M = "m"
    KM = "Km"

    def to_array(self):
        array = []
        for item in DistanceUnit:
            array.append(item.value)
        return array


class PowerUnit(Enum):
    WALT = "Walt"

    def to_array(self):
        array = []
        for item in PowerUnit:
            array.append(item.value)
        return array

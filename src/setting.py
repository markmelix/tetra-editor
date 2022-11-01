from typing import OrderedDict
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QCheckBox, QLineEdit

from utils import EnhancedQComboBox, EnhancedQSpinBox


class Setting:
    """Настройка модуля"""

    def __init__(self, name, description="", value=None):
        self.name = name
        self.description = description
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class StringSetting(Setting):
    """Настройка, принимающая в качестве значения строку"""

    def __init__(self, name=None, description="", value=None):
        super().__init__(name, description, value)

    def widget(self):
        widget = QLineEdit()
        widget.setText(self.value)
        widget.textChanged.connect(self.set_value)
        widget.set_value = lambda v: widget.setText(v)
        return widget


class IntSetting(Setting):
    """Настройка, принимающая в качестве значения целое число"""

    def __init__(
        self,
        name=None,
        description="",
        value=0,
        min_value=0,
        max_value=9999,
        step=1,
    ):
        super().__init__(name, description, value)

        self.min_value = min_value
        self.max_value = max_value
        self.step = step

    def set_value(self, value):
        self.value = int(value)

    def get_value(self):
        return int(self.value)

    def widget(self):
        widget = EnhancedQSpinBox()

        widget.setFocusPolicy(Qt.StrongFocus)
        widget.setMinimum(self.min_value)
        widget.setMaximum(self.max_value)
        widget.setSingleStep(self.step)
        widget.setValue(self.get_value())

        widget.textChanged.connect(self.set_value)
        widget.set_value = lambda v: widget.setValue(v)

        return widget


class BoolSetting(Setting):
    """Настройка, принимающая в качестве значение True или False"""

    def __init__(self, name=None, description="", value=False):
        super().__init__(name, description, value)

    def set_value(self, value):
        self.value = bool(int(value))

    def get_value(self):
        return bool(int(self.value))

    def widget(self):
        widget = QCheckBox()
        widget.setChecked(self.get_value())
        widget.setText("Включен" if self.value else "Выключен")
        widget.stateChanged.connect(
            lambda state: widget.setText("Включен" if state else "Выключен")
        )
        widget.stateChanged.connect(self.set_value)
        widget.set_value = lambda v: widget.setCheckState(v)
        return widget


class SellectionSetting(Setting):
    """Настройка, принимающая в качестве значение один строковый элемент из
    списка возможных элементов"""

    def __init__(self, name=None, description="", value=None, values=OrderedDict()):
        super().__init__(name, description, value)

        self.values = values

    def get_value(self):
        return self.values[self.value]

    def widget(self):
        widget = EnhancedQComboBox()
        widget.setFocusPolicy(Qt.StrongFocus)
        widget.insertItems(0, self.values.keys())
        if self is not None:
            widget.setCurrentText(self.value)
        widget.currentTextChanged.connect(self.set_value)
        widget.set_value = lambda v: widget.setCurrentText(v)
        return widget


class FileSetting(Setting):
    """Настройка, принимающая в качестве значения путь до файла в файлововй
    системе"""

    def __init__(self, name=None, description="", value=None, ext=None):
        super().__init__(name, description, value)

        self.ext = ext

    def widget(self):
        widget = QLineEdit()
        widget.setText(self.value)
        widget.textChanged.connect(self.set_value)
        widget.set_value = lambda v: widget.setText(v)
        return widget


class ColorSetting(Setting):
    """Настройка, принимающая в качестве значения цвет"""

    def __init__(self, name=None, description="", value=None):
        super().__init__(name, description, value)

    def get_value(self):
        return QColor(self.value)

    def widget(self):
        widget = QLineEdit()
        widget.setText("" if self.value is None else self.value)
        widget.textChanged.connect(self.set_value)
        widget.set_value = lambda v: widget.setText(v)
        return widget

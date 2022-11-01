from enum import Enum, auto
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QComboBox, QFrame, QSizePolicy, QSpinBox

SaveStatus = Enum("SaveStatus", ["SAVED", "CANCELED"])


class FileType(Enum):
    UNKNOWN = auto()
    PYTHON = auto()
    JSON = auto()
    SQL = auto()
    XML = auto()
    HTML = auto()
    YAML = auto()
    MARKDOWN = auto()

    @classmethod
    def from_ext(cls, ext):
        """Возвращает вариант перечисления FileType в соответствии с переданным
        расширением файла"""

        assignments = {
            "py": cls.PYTHON,
            "json": cls.JSON,
            "sql": cls.SQL,
            "xml": cls.XML,
            "html": cls.HTML,
            "yaml": cls.YAML,
            "md": cls.MARKDOWN,
        }

        return assignments[ext] if ext in assignments else cls.UNKNOWN


class QHSeparationLine(QFrame):
    """Просто линия для разделения элементов"""

    def __init__(self):
        super().__init__()

        self.setMinimumWidth(1)
        self.setFixedHeight(20)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class EnhancedQComboBox(QComboBox):
    """QComboBox с выключенным скроллингом при наведении мыши"""

    def __init__(self, scrollWidget=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scrollWidget = scrollWidget
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            return QComboBox.wheelEvent(self, event)
        event.ignore()


class EnhancedQSpinBox(QSpinBox):
    """QSpinBox с выключенным скроллингом при наведении мыши"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            return QSpinBox.wheelEvent(self, event)
        event.ignore()

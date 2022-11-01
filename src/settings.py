from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from event import Event
from utils import QHSeparationLine

import csv


class ModuleSettings(QWidget):
    def __init__(self, module, parent=None):
        super().__init__(parent)

        self.module = module

        self.main_layout = QVBoxLayout()

        self.title_layout = QHBoxLayout()

        self.title = QLabel(module.name)
        self.title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        self.title.setToolTip(module.description)
        self.title.setWordWrap(True)

        self.state = QCheckBox()
        self.state.setText("Включен" if module.enabled else "Выключен")
        self.state.setDisabled(not module.can_disable)
        self.state.setChecked(module.enabled)
        self.state.stateChanged.connect(self.turn_module)

        self.title_layout.addWidget(self.title, 10)
        self.title_layout.addWidget(self.state, 1)

        self.main_layout.addLayout(self.title_layout)

        for id, setting in module.settings.items():
            title = QLabel(id if setting.name is None else setting.name)
            title.setWordWrap(True)
            title.setStyleSheet("font-size: 12pt; font-style: bold;")

            info_layout = QVBoxLayout()
            info_layout.addWidget(title)

            if setting.description != "":
                desc = QLabel(setting.description)
                desc.setWordWrap(True)
                desc.setStyleSheet("font-size: 10pt; font-style: italic;")

                info_layout.addWidget(desc)

            info_widget = QWidget()
            info_widget.setLayout(info_layout)

            control_widget = setting.widget()
            control_widget.setObjectName(f"{module.id}__{id}")
            control_widget.setProperty("setting", setting)
            control_widget.setFixedWidth(200)

            reset_setting = QPushButton("Сбросить")
            reset_setting.setProperty("setting", control_widget.objectName())
            reset_setting.clicked.connect(self.reset_setting)

            layout = QHBoxLayout()
            layout.addWidget(info_widget, 5)
            layout.addWidget(control_widget, 5)
            layout.addWidget(reset_setting, 0)

            widget = QWidget()
            widget.setLayout(layout)

            self.main_layout.addWidget(widget)

        self.setLayout(self.main_layout)

    def turn_module(self, state):
        self.state.setText("Включен" if state else "Выключен")
        self.module.toggle(state)

    def reset_setting(self):
        button = self.sender()

        id = button.property("setting")
        clean_id = id.split("__")[-1]

        default = self.module.default_settings[clean_id]

        widget = self.findChild(QWidget, id, Qt.FindChildrenRecursively)
        widget.set_value(default.value)


class Settings(QMainWindow):
    def __init__(self, core):
        super().__init__()

        self.setGeometry(300, 100, 700, 600)
        self.setWindowTitle("Настройки")

        self.core = core
        self.layout = QVBoxLayout()

        self.title = QLabel("Настройки")
        self.title.setStyleSheet("font-size: 17pt;")

        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)

        self.import_button = QPushButton("Импортировать из CSV")
        self.import_button.clicked.connect(self.import_settings)

        self.export_button = QPushButton("Экспортировать в CSV")
        self.export_button.clicked.connect(self.export_settings)

        self.port_layout = QHBoxLayout()
        self.port_layout.addWidget(self.import_button)
        self.port_layout.addWidget(self.export_button)

        self.port_widget = QWidget()
        self.port_widget.setLayout(self.port_layout)

        self.layout.addWidget(self.port_widget)

        self.layout.addWidget(QHSeparationLine())

        for module in filter(
            lambda m: m.can_disable or len(m.settings) != 0, core.modules.values()
        ):
            settings = ModuleSettings(module, self)
            self.layout.addWidget(settings)
            self.layout.addWidget(QHSeparationLine())

        self.layout_widget = QWidget()
        self.layout_widget.setLayout(self.layout)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.layout_widget)

        self.setCentralWidget(self.scroll)
        self.installEventFilter(self)

    def save(self):
        for module in self.core.modules.values():
            module.save_settings()
        self.core.raise_event(Event.SETTINGS_SAVED)

    def closeEvent(self, event) -> None:
        self.save()
        event.accept()

    def import_settings(self):
        self.save()

        path, _ = QFileDialog.getOpenFileName(
            self, "Импорт файла", "settings.csv", "CSV Файлы (*.csv)", ""
        )

        if path == "":
            return

        modules = self.core.modules

        with open(path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar="'")
            for id, value in reader:
                module = id.split(":")[0]
                id = id.split(":")[-1]
                modules[module][id].value = value

        self.core.raise_event(Event.SETTINGS_SAVED)
        self.close()

    def export_settings(self):
        self.save()

        path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт файла", "settings.csv", "CSV Файлы (*.csv)", ""
        )

        if path == "":
            return

        cur = self.core.con.cursor()

        with open(path, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar='"')
            rows = cur.execute("SELECT id, value FROM settings").fetchall()
            writer.writerows(rows)

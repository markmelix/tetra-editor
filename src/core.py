import modules

from buffer import BufManager, GuiBuffer
from modules import MODULES
from event import Event, apply_event
from module import Module
from settings import Settings
from ui import Ui_MainWindow
from utils import SaveStatus

from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox


class Core(QMainWindow, Ui_MainWindow):
    """Ядро редактора, собирающее все компоненты программы в единую систему"""

    def __init__(self):
        super().__init__()

        self.modules = {}

        self.init_event_system()
        self.init_ui()
        self.init_modules()
        self.init_buffer_manager()

    def init_event_system(self):
        """Инициализирует систему событий"""

        self.events = []

    def last_event(self):
        """Возвращает последнее вызванное событие"""

        try:
            return self.events[-1]
        except IndexError:
            return None

    def init_buffer_manager(self):
        """Инициализирует систему управления буферами редактора"""

        self.buffers = BufManager()
        self.buffers.add_empty(self.gui_buffer_instance())
        self.raise_event(Event.NEW_BUFFER_CREATED)

    def init_ui(self):
        """Инициализирует пользовательский интерфейс редактора"""
        self.setupUi(self)
        self.setCentralWidget(self.global_layout_widget)

    def init_module(self, module):
        """Инициализирует встроенный модуль редактора"""

        # Трансформировать название_модуля в НазваниеМодуля
        module_class = "".join(word.title() for word in module.split("_"))

        return eval(f"modules.{module}.{module_class}(self)")

    def init_modules(self):
        """Инициализирует встроенные в редактор модули"""

        for module in MODULES:
            mod = self.init_module(module)

            if module == "database":
                mod.load()
            else:
                mod.load_if_enabled()

            self.modules[module] = mod

    def unload_modules(self):
        """Выгружает встроенные в редактор модули"""

        for module in filter(Module.is_loaded, self.modules.values()):
            module.unload()

    def refresh_modules(self):
        """Обновляет состояние встроенных в редактор модулей"""

        for module in filter(Module.is_loaded, self.modules.values()):
            module.refresh()

    def find_module(self, id):
        """Возвращает модуль с заданным id"""
        return self.modules[id]

    def closeEvent(self, event):
        """Делает то, что нужно сделать перед закрытием программы"""

        self.unload_modules()
        event.accept()

    def raise_event(self, event):
        """Вызывает событие"""

        self.events.append(event)
        self.refresh_modules()

    def gui_buffer_instance(self):
        """Создает и возвращает пустой графический буфер редактирования"""
        return GuiBuffer()

    __gui_buffer_instance = gui_buffer_instance

    @apply_event(Event.NEW_BUFFER_CREATED)
    def create_new_file(self):
        """Создает новый файл"""

        self.buffers.add_empty(self.gui_buffer_instance())

    def save_file(self, buffer=None, raise_event=True):
        """Сохраняет открытый файл"""

        if buffer is None:
            buffer = self.buffers.current()

        if buffer.file is None:
            status = self.save_file_as(buffer, raise_event=raise_event)
        else:
            buffer.sync()
            status = SaveStatus.SAVED

        if raise_event:
            self.raise_event(Event.FILE_SAVED)

        return status

    def save_file_as(self, buffer=None, raise_event=True):
        """Сохраняет открытый файл как"""

        options = QFileDialog.Options()

        path, status = QFileDialog.getSaveFileName(
            self, "Сохранить файл как", "", "", options=options
        )
        status = SaveStatus.SAVED if bool(status) else SaveStatus.CANCELED

        if path == "":
            return SaveStatus.CANCELED

        if buffer is None:
            buffer = self.buffers.current()

        buffer.set_sync_file(path)
        buffer.sync()

        if raise_event:
            self.raise_event(Event.FILE_SAVED_AS)

        return status

    @apply_event(Event.FILE_OPENED)
    def open_file(self):
        """Открывает существующий файл"""

        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "", "")

        if path == "":
            return

        self.buffers.add(self.gui_buffer_instance(), sync_file=path)

    @apply_event(Event.SETTINGS_OPENED)
    def open_settings(self):
        """Открывает окно настроек редактора"""

        self.settings = Settings(self)
        self.settings.show()

    @apply_event(Event.ABOUT_DIALOG_OPENED)
    def open_about_dialog(self):
        """Открывает окно "О программе" """

        QMessageBox.about(
            self,
            "Tetra Code Editor",
            "Модульный редактор кода с графическим интерфейсом.\nАвтор: Меликсетян Марк.",
        )

from enum import Enum
from pathlib import Path
import charset_normalizer

from utils import FileType

DEFAULT_EMPTY_BUFFER_NAME = "Безымянный"

# Перечисление возможных синхронизаций. Сихронизировать можно либо текст буфера
# с файлом (Sync.TO_FILE), либо содержимое файла с буфером (Sync.FROM_FILE)
Sync = Enum("Sync", ["FROM_FILE", "TO_FILE"])


class BufferException:
    """Класс всех исключений, связанных с буферами"""


class NoSyncFileError(BufferException):
    """Исключение, вызываемое при попытке синхронизировать текстовый буфер с не
    указанным файлом синхронизации"""


class EncodingGuessError(BufferException):
    """Исключение, вызываемое при неудачной попытке определить кодировку файла"""


class Buffer:
    """Абстрактный текстовый буфер редактора"""

    def __init__(
        self,
        empty_name=DEFAULT_EMPTY_BUFFER_NAME,
        sync_file=None,
        text="",
    ):
        """Инициализирует буфер

        Параметры:
        empty_name - название буфера, не имеющего файла для синхронизации
        sync_file  - файл для синхронизации
        text       - начальный текст буфера

        """

        self.empty_name = empty_name
        self.text = text
        self.file = None
        self.file_encoding = None
        self.full_encoding = None
        self.synchronized = sync_file is not None

        self.refresh_name()

        if sync_file is not None:
            self.set_sync_file(sync_file)
            self.sync(Sync.FROM_FILE)

    def __str__(self):
        return f"{self.__class__.__name__}(name='{self.name}', synchronized={self.synchronized})"

    def set_sync_file(self, file):
        Path(file).touch()
        self.file = file
        self.file_encoding = self.determine_encoding()

    def set_text(self, text):
        """Устанавливает текст буфера"""

        self.text = text
        self.desync()

    def determine_encoding(self):
        """Пытается определить кодировку привязанного к буферу файла
        сихнронизации. Вызывает исключение NoSyncFileError, если файл для
        синхронизации не установлен"""

        if self.file is None:
            raise NoSyncFileError

        guess = charset_normalizer.from_path(self.file).best()

        if guess is None:
            return None

        return guess.encoding

    def sync(self, kind=Sync.TO_FILE):
        """Синхронизирует текст буфера с файлом (kind=Sync.TO_FILE), либо
        содержимое файла с буфером (kind=Sync.FROM_FILE). Вызывает исключение
        NoSyncFileError, если файл для синхронизации не установлен или
        EncodingGuessError, если не удалось определить его кодировку"""

        if self.file is None:
            raise NoSyncFileError

        if kind == Sync.TO_FILE:
            mode = "w"
        else:
            mode = "r"

        if self.file_encoding is None:
            mode += "b"

        file = open(self.file, mode=mode, encoding=self.file_encoding)

        if kind == Sync.TO_FILE:
            file.write(self.text)
        else:
            self.text = file.read()
            self._sync()

        file.close()

        self.synchronized = True

        self.refresh_name()

    def _sync(self):
        """Устанавливает флаг синхронизации буфера с файлом синхронизации в
        True. Данный метод должен быть использован только классом Buffer либо в
        исключительных случаях, чтобы по особому обработать буфер"""

        self.synchronized = True

    def desync(self):
        """Десинхронизирует буфер с файлом синхронизации"""
        self.synchronized = False

    def refresh_name(self):
        """Обновляет имя буфера в соответствии с именем файла синхронизации"""
        self.name = self.empty_name if self.file is None else self.file.split("/")[-1]

    def file_type(self):
        """Возвращает вариант перечисления FileType в соответствии с расширением
        прикрепленного к буферу файла синхронизации"""
        try:
            return FileType.from_ext(self.file.split(".")[-1])
        except:
            return None

    def is_empty(self):
        """Возвращает True, если буфер не имеет прикрепленного файла и является
        пустым, иначе - False"""
        return self.name == self.empty_name and self.text == ""


class BufManager:
    """Менеджер управления текстовыми буферами"""

    def __init__(self):
        self.buffers = {}

    def add(self, gui_link, *args, **kwargs):
        """Добавить буфер с заданными параметрами.

        Параметры:
        gui_link - ссылка на графический буфер, с которым
                   необходимо связать созданный абстрактный буфер
        """

        self.buffers[gui_link] = Buffer(*args, **kwargs)
        self.current_link = gui_link

    def current(self):
        return self.buffers[self.current_link]

    def switch(self, gui_link):
        self.current_link = gui_link

    def add_empty(self, gui_link):
        """Добавить пустой буфер"""
        self.add(gui_link)

    def remove(self, gui_link, new_current=None):
        """Удаляет буфер"""
        del self.buffers[gui_link]

        if gui_link != self.current_link:
            return

        if new_current is None:
            self.current_link = next(iter(self.buffers.keys()))
        else:
            self.current_link = new_current

    def __len__(self):
        return len(self.buffers)

    def __getitem__(self, gui_link):
        """Возвращает буфер, привязанный к данному графическому буферу"""
        return self.buffers[gui_link]


class GuiBuffer:
    """Общий класс графических буферов"""

    def __init__(self):
        self.buffer = ""
        self.supports_syntax_highlighting = False

    def text_changed(self, func):
        self.text_changed_hook = func()

    def set_text(self, text):
        self.buffer = text
        self.text_changed_hook()

    def get_text(self):
        return self.buffer

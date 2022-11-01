from typing import OrderedDict
from buffer import GuiBuffer
from utils import FileType
from module import Module
from PyQt5.Qsci import *
from event import Event
from setting import *


NAME = "Буфер редактирования"
DESCRIPTION = "В буфере редактирования происходит редактирование файлов"

EOL_UNIX = "Unix (LF)"
EOL_WINDOWS = "Windows (CR LF)"

DEFAULT_SETTINGS = {
    "syntax_highlighting": BoolSetting(
        name="Подсветка кода",
        description="После отключения данной настройки необходим перезапуск редактора",
        value=True,
    ),
    "line_numbers": BoolSetting(
        name="Нумерация строк",
        value=True,
    ),
    "wrap_mode": SellectionSetting(
        name="Перенос",
        value="Отключен",
        values=OrderedDict(
            [
                ("Отключен", QsciScintilla.WrapNone),
                ("По словам", QsciScintilla.WrapWord),
                ("По символам", QsciScintilla.WrapCharacter),
                ("По пробелам", QsciScintilla.WrapWhitespace),
            ]
        ),
    ),
    "wrap_indent_mode": SellectionSetting(
        name="Отступ при переносе",
        value="Отключен",
        values=OrderedDict(
            [
                ("Отключен", QsciScintilla.WrapIndentSame),
                ("Включен", QsciScintilla.WrapWord),
            ]
        ),
    ),
    "eol_mode": SellectionSetting(
        name="Режим EOL",
        description="Определяет конец каждой строки",
        value=EOL_UNIX,
        values=OrderedDict(
            [
                (EOL_UNIX, QsciScintilla.EolUnix),
                (EOL_WINDOWS, QsciScintilla.EolWindows),
            ]
        ),
    ),
    "eol_visibility": BoolSetting(
        name="Видимость EOL",
        description="При включении данной настройки в конце каждой строки будет индикатор ее конца",
        value=False,
    ),
    "indentation_use_tabs": BoolSetting(
        name="Использовать табы вместо пробелов",
        value=True,
    ),
    "indentation_size": IntSetting(
        name="Размер отступа",
        value=4,
        min_value=1,
    ),
    "indentation_guides": BoolSetting(
        name="Линии отступов",
        description="Показывать пунктирные вертикальные линии для обозначения уровней отступов",
        value=False,
    ),
    "tab_indents": BoolSetting(
        name="Выравнивать отступ на пробелах",
        description="""Влияет на поведение клавиши TAB, когда курсор окружен
пробелами. В выключенном состоянии данной настройки, редактор просто вставляет n
символов отступа (пробелы или табы) при нажатии клавиши TAB. Но если настройка
включена, редактор перемещает первый не пробельный символ на следующий уровень
отступа.""",
        value=True,
    ),
    "auto_indent": BoolSetting(
        name="Автоматический отступ",
        description="""При вставке новой строки автоматический отступ перемещает
курсор на тот же уровень отступа, что и предыдущая строка. Данная настройка
может быть игнорирована при влюченной подсветке кода""",
        value=True,
    ),
    "caret_line_visible": BoolSetting(
        name="Подсветка строки, на которой расположен курсор",
        value=True,
    ),
    "caret_line_background_color": ColorSetting(
        name="Цвет подсвеченной строки",
        value="#1fff0000",
    ),
    "caret_width": IntSetting(
        name="Ширина курсора",
        description="Ширина курсора в пикселях. Ширина равная нулю делает курсор невидимым!",
        value=1,
    ),
}


class EnhancedGuiBuffer(QsciScintilla, GuiBuffer):
    """Усовершенствованный графический буфер редактирования"""

    def __init__(self, settings, buffer=None):
        super().__init__()

        self.buffer = buffer
        self.apply_settings(settings)

    def apply_settings(self, settings):
        if self.buffer is not None and settings["syntax_highlighting"].get_value():
            self.apply_syntax_highlighting()

        assignments = {
            "line_numbers": self.apply_line_numbers,
            "wrap_mode": self.setWrapMode,
            "wrap_indent_mode": self.setWrapIndentMode,
            "eol_mode": self.setEolMode,
            "eol_visibility": self.setEolVisibility,
            "indentation_use_tabs": self.setIndentationsUseTabs,
            "indentation_size": self.setTabWidth,
            "indentation_guides": self.setIndentationGuides,
            "tab_indents": self.setTabIndents,
            "auto_indent": self.setAutoIndent,
            "caret_line_visible": self.setCaretLineVisible,
            "caret_line_background_color": self.setCaretLineBackgroundColor,
            "caret_width": self.setCaretWidth,
        }

        for id, activator in assignments.items():
            activator(settings[id].get_value())

        self.settings = settings

    def apply_line_numbers(self, yes):
        if not yes:
            self.setMarginWidth(1, 0)
            return

        self.setMarginWidth(1, 35)
        self.setMarginType(1, QsciScintilla.NumberMargin)

    def apply_syntax_highlighting(self):
        if self.buffer is None:
            return

        file_type = self.buffer.file_type()

        lexers = {
            FileType.PYTHON: QsciLexerPython,
            FileType.JSON: QsciLexerJSON,
            FileType.SQL: QsciLexerSQL,
            FileType.XML: QsciLexerXML,
            FileType.HTML: QsciLexerHTML,
            FileType.YAML: QsciLexerYAML,
            FileType.MARKDOWN: QsciLexerMarkdown,
        }

        if file_type not in lexers:
            return

        self.setLexer(lexers[file_type](self))

    def text_changed(self, func):
        self.textChanged.connect(func)

    def set_text(self, text):
        try:
            self.setText(text)
        except TypeError:
            self.setText(text.decode("utf-8", "backslashreplace"))

    def get_text(self):
        return self.text()

    def refresh(self, settings, event, buffer=None):
        if (
            event in {Event.SETTING_CHANGED, Event.SETTINGS_SAVED}
            or self.settings != settings
        ):
            self.apply_settings(settings)

        if self.buffer is not buffer:
            self.buffer = buffer

        if event in {Event.FILE_OPENED, Event.FILE_SAVED_AS}:
            self.apply_syntax_highlighting()


class EditBuffer(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def load(self):
        super().load()

        def core_gui_buffer_instance():
            return EnhancedGuiBuffer(self.settings)

        self.core.gui_buffer_instance = core_gui_buffer_instance

    def unload(self):
        super().unload()

        self.core.gui_buffer_instance = self.core._Core__gui_buffer_instance

    def refresh(self):
        super().refresh()

        core = self.core
        event = core.last_event()
        buffers = core.buffers.buffers

        for gui_buffer, abs_buffer in buffers.items():
            gui_buffer.refresh(self.settings, event, abs_buffer)

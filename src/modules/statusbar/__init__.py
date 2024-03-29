from PyQt5.QtWidgets import QLabel
from module import Module
from event import Event
from modules.edit_buffer import EOL_WINDOWS
from setting import BoolSetting, StringSetting


NAME = "Statusbar"
DESCRIPTION = "Statusbar has information about opened file"

DEFAULT_SETTINGS = {
    "delimiter": StringSetting(
        name="Component delimeter",
        value=" | ",
    ),
    "show_name": BoolSetting(
        name="Show buffer name",
        value=True,
    ),
    "show_eol": BoolSetting(
        name="Show EOL",
        description="EOL is the end of each text line of the file, may be either LF (\\n), or CR LF (\\r\\n)",
        value=True,
    ),
    "show_encoding": BoolSetting(
        name="Show file encoding",
        value=True,
    ),
}

TRIGGER_EVENTS = (
    Event.NEW_BUFFER_CREATED,
    Event.FILE_SAVED_AS,
    Event.FILE_OPENED,
    Event.TAB_CHANGED,
    Event.TAB_CLOSED,
    Event.SETTINGS_SAVED,
)


class Statusbar(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core)

    def load(self):
        super().load()

        self.widget = QLabel()
        self.core.statusBar().addWidget(self.widget)
        self.refresh()

    def unload(self):
        super().unload()

        self.core.statusBar().removeWidget(self.widget)

    def generate(self, buffer):
        """Generates and returns statusbar text"""

        detailed_name = (
            buffer.name
            if buffer.file is None
            else "/".join(buffer.file.split("/")[-2:])
        )
        eol = self.core.find_module("edit_buffer")["eol_mode"].value
        eol = "CR LF" if eol == EOL_WINDOWS else "LF"
        encoding = (
            "???"
            if buffer.file_encoding is None
            else buffer.file_encoding.replace("_", "-").upper()
        )

        comps = (
            ("show_name", detailed_name),
            ("show_eol", eol),
            ("show_encoding", encoding),
        )

        enabled = []

        for setting, comp in comps:
            if self[setting].get_value():
                enabled.append(comp)

        return self["delimiter"].value.join(enabled)

    def refresh(self):
        super().refresh()

        core = self.core

        if core.last_event() not in TRIGGER_EVENTS:
            return

        try:
            info = self.generate(core.buffers.current())
            self.widget.setText(info)
        except KeyError:
            pass

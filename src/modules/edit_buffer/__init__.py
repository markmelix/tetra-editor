from PyQt5.Qsci import *
from event import Event
from module import Module


NAME = "Буфер редактирования"
DESCRIPTION = "В буфере редактирования происходит редактирование файлов"

DEFAULT_SETTINGS = []


class EditBuffer(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def sync_current(self):
        core = self.core
        current, buffer = core.buffers.current, core.buffer

        current.set_text(buffer.text())

        core.raise_event(Event.BUFFER_TEXT_CHANGED)

        self.refresh()

    def load(self):
        super().load()

        core = self.core
        buffer = core.buffer

        buffer.textChanged.connect(self.sync_current)

        self.refresh()

    def unload(self):
        super().unload()

    def highlight_synchronized(self):
        core = self.core
        current_buffer, label = core.buffers.current, core.label

        if current_buffer.synchronized:
            label.setStyleSheet("color: black;")
        else:
            label.setStyleSheet("color: red;")

    def refresh(self):
        super().refresh()

        core = self.core
        gui_buffer, label, buffers, event = (
            core.buffer,
            core.label,
            core.buffers,
            core.last_event(),
        )
        current_buffer = buffers.current

        current_buffer.refresh_name()

        label.setText(current_buffer.name)

        if event in {Event.FILE_OPENED, Event.NEW_BUFFER_CREATED}:
            gui_buffer.setText(current_buffer.text)

        if event == Event.FILE_OPENED:
            current_buffer._sync()

        self.highlight_synchronized()

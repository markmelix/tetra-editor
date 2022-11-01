from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
from PyQt5.Qsci import *
from event import Event
from module import Module
from utils import SaveStatus


NAME = "Таббар"
DESCRIPTION = "Таббар позволяет переключаться между буферами"

DEFAULT_SETTINGS = {}


class Tabbar(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def ask_for_save(self):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Question)
        dialog.setText("Файл был изменен.")
        dialog.setInformativeText("Сохранить изменения?")
        dialog.setStandardButtons(
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        dialog.setDefaultButton(QMessageBox.Save)

        return dialog.exec()

    def remove_tab_and_buffer(self, idx):
        core = self.core
        tabbar = core.tabbar
        gui_buffer = tabbar.widget(idx)

        tabbar.removeTab(idx)
        core.buffers.remove(
            gui_buffer, new_current=tabbar.widget(tabbar.currentIndex())
        )

        core.raise_event(Event.TAB_CLOSED)

    def close_tab(self, idx):
        buffers = self.core.buffers

        if len(buffers) == 1:
            return

        tabbar = self.core.tabbar
        gui_buffer = tabbar.widget(idx)
        buffer = buffers[gui_buffer]

        if buffer.is_empty() or buffer.synchronized:
            self.remove_tab_and_buffer(idx)
            return

        answer = self.ask_for_save()

        if answer == QMessageBox.Cancel or (
            answer == QMessageBox.Save
            and self.core.save_file(buffer, raise_event=False) == SaveStatus.CANCELED
        ):
            return

        self.remove_tab_and_buffer(idx)

    def change_current(self, idx):
        # return
        buffers = self.core.buffers
        tabbar = self.core.tabbar
        gui_buffer = tabbar.widget(idx)
        # buffer = buffers[gui_buffer]
        buffers.current_link = gui_buffer
        self.core.raise_event(Event.TAB_CHANGED)

    def load(self):
        super().load()

        tabbar = self.core.tabbar

        tabbar.currentChanged.connect(self.change_current)
        tabbar.tabCloseRequested.connect(self.close_tab)

        self.refresh()

    def unload(self):
        super().unload()

    def sync_buffer(self, gui_buffer=None):
        core = self.core
        buffers = core.buffers

        if gui_buffer is None:
            gui_buffer, abs_buffer = buffers.current_link, buffers.current()
        else:
            abs_buffer = buffers[gui_buffer]

        abs_buffer.set_text(gui_buffer.get_text())

        if core.last_event() != Event.FILE_OPENED:
            core.raise_event(Event.BUFFER_TEXT_CHANGED)
        else:
            core.raise_event(None)

        self.refresh()

    def highlight_desynced(self):
        core = self.core
        tabbar = core.tabbar.tabBar()
        tab = tabbar.currentIndex()
        current = core.buffers.current()
        synced = current.synchronized

        tabbar.setTabTextColor(tab, QColor(0, 0, 0) if synced else QColor(255, 0, 0))

    def refresh(self):
        super().refresh()

        core = self.core
        tabbar = core.tabbar
        event = core.last_event()

        if event in {Event.FILE_OPENED, Event.NEW_BUFFER_CREATED}:
            current_link = core.buffers.current_link
            current = core.buffers.current()

            current_link.text_changed(self.sync_buffer)
            current_link.set_text(current.text)

            tabbar.insertTab(0, current_link, current.name)
            tabbar.setCurrentIndex(0)
            core.raise_event(Event.TAB_CREATED)

        if event == Event.FILE_SAVED_AS:
            tabbar.setTabText(tabbar.currentIndex(), core.buffers.current().name)

        if event in {
            Event.FILE_OPENED,
            Event.FILE_SAVED_AS,
            Event.FILE_SAVED,
            Event.TAB_CREATED,
        }:
            core.buffers.current()._sync()

        if event in {
            Event.NEW_BUFFER_CREATED,
            Event.BUFFER_TEXT_CHANGED,
            Event.FILE_SAVED_AS,
            Event.FILE_SAVED,
            Event.TAB_CHANGED,
            Event.TAB_CREATED,
        }:
            self.highlight_desynced()

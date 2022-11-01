from module import Module

NAME = "Меню"
DESCRIPTION = "Делает кнопки меню функциональными"

DEFAULT_SETTINGS = {}


class Menu(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def load(self):
        super().load()

        core = self.core

        self.links = (
            (core.new_file_action, lambda: core.create_new_file()),
            (core.save_file_action, lambda: core.save_file()),
            (core.save_file_as_action, lambda: core.save_file_as()),
            (core.open_file_action, lambda: core.open_file()),
            (core.settings_action, lambda: core.open_settings()),
            (core.about_action, lambda: core.open_about_dialog()),
        )

        for action, func in self.links:
            action.triggered.connect(func)

    def unload(self):
        super().unload()

        for action, func in self.links:
            action.triggered.disconnect(func)

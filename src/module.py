from copy import deepcopy


class Module:
    """Модуль программы, или, иными словами, настраиваемый компонент программы с
    минимальным дополняющим функционалом"""

    def __init__(self, name, description, default_settings, core, can_disable=True):
        self.name = name
        self.description = description
        self.default_settings = default_settings
        self.core = core
        self.can_disable = can_disable

        self.id = self.__module__.split(".")[-1]
        self.settings = deepcopy(default_settings)

        self.enabled = True
        self.loaded = False

    # Подобные приватные переменные нужны, чтобы можно было переопределять
    # методы класса без бесконечных рекурсий.
    __init = __init__

    def set(self, setting_id, new_value):
        """Устанавливает новое значение настройки с заданным идентификатором"""
        self.settings[setting_id].value = new_value

    def __getitem__(self, setting_id):
        """Возвращает настройку с данным идентификатором"""
        return self.settings[setting_id]

    def is_loaded(self):
        """Возвращает состояние модуля (загружен в программу или нет)"""
        return self.loaded

    def toggle(self, state):
        """Включает модуль, если state - True, иначе выключает"""
        if state:
            self.enable()
        else:
            self.disable()

    def disable(self):
        """Выключает и выгружает модуль"""
        self.enabled = False
        self.unload()

    __disable = disable

    def enable(self):
        """Включает и загружает модуль"""
        self.enabled = True
        self.load()

    __enable = enable

    def load_if_enabled(self):
        """Загружает модуль при условии, что он включен"""
        if self.enabled:
            self.load()

    def load(self):
        """Загружает модуль в программу"""
        self.loaded = True

    __load = load

    def unload(self):
        """Выгружает модуль из программы"""
        self.loaded = False

    __unload = unload

    def refresh(self):
        """Обновляет модуль. Полезно вызывать данный метод после вызова
        какого-либо события в программе, чтобы обновить состояние модуля в
        соответствии с этим событием"""
        pass

    __refresh = refresh

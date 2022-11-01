from module import Module
from setting import *
from copy import deepcopy

import sqlite3

NAME = "База данных"
DESCRIPTION = "Сохраняет состояние настроек редактора в базу данных"

DB_FILE = "tetra.db"

DEFAULT_SETTINGS = {}

CREATE_TABLES_QUERY = """
CREATE TABLE IF NOT EXISTS modules (
	id string PRIMARY KEY,
	enabled boolean
);
CREATE TABLE IF NOT EXISTS settings (
    id string PRIMARY KEY,
    module string,
    value string
);
"""


class Database(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def connect(self):
        """Устанавливает соединение с базой данных"""

        self.con = sqlite3.connect(DB_FILE)

    def create_tables(self):
        """Создает нужные таблицы в базе данных, если они ещё не были созданы"""

        self.con.executescript(CREATE_TABLES_QUERY)

    def inject_features(self):
        """Внедряет функционал для работы с базой данных в программу"""

        con = self.con
        cur = self.con.cursor()

        def module_init(mod, *args, **kwargs):
            Module._Module__init(mod, *args, **kwargs)

            cur.execute(
                "INSERT OR IGNORE INTO modules VALUES (?,?)", (mod.id, mod.enabled)
            )

            mod.enabled = bool(
                cur.execute(
                    "SELECT enabled FROM modules WHERE id=?", (mod.id,)
                ).fetchone()[0]
            )

            for setting_id, setting in mod.default_settings.items():
                id, module, value = f"{mod.id}:{setting_id}", mod.id, setting.value
                cur.execute(
                    "INSERT OR IGNORE INTO settings VALUES (?,?,?)", (id, module, value)
                )

            def row_to_setting(row):
                id, value = row
                id = id.split(":")[-1]
                setting = deepcopy(mod.default_settings[id])
                setting.value = value

                return id, setting

            setting_rows = cur.execute(
                "SELECT id,value FROM settings WHERE module IN (SELECT id FROM modules WHERE id=?)",
                (mod.id,),
            ).fetchall()

            mod.settings = {
                id: setting for id, setting in map(row_to_setting, setting_rows)
            }

            con.commit()

        def update_enabled_state(mod, state):
            cur.execute("UPDATE modules SET enabled=? WHERE id=?", (state, mod.id))
            con.commit()

        def module_enable(mod, *args, **kwargs):
            Module._Module__enable(mod, *args, **kwargs)
            update_enabled_state(mod, True)

        def module_disable(mod, *args, **kwargs):
            Module._Module__disable(mod, *args, **kwargs)
            update_enabled_state(mod, False)

        def module_save_settings(mod):
            """Сохраняет настройки модуля в базу данных"""
            for id, setting in mod.settings.items():
                cur.execute(
                    "UPDATE settings SET value=? WHERE id=?",
                    (setting.value, f"{mod.id}:{id}"),
                )
                con.commit()

        Module.__init__ = module_init
        Module.enable = module_enable
        Module.disable = module_disable
        Module.save_settings = module_save_settings

        self.core.con = self.con

    def disconnect(self):
        """Прерывает соединение с базой данных"""

        self.core.con.close()

    def eject_features(self):
        """Убирает функционал для работы с базой данных из программы"""

        Module.__init__ = Module._Module__init
        Module.enable = Module._Module__enable
        Module.disable = Module._Module__disable

        del Module.save_settings

        del self.core.con

    def load(self):
        super().load()

        self.connect()
        self.create_tables()
        self.inject_features()

    def unload(self):
        super().unload()

        self.disconnect()
        self.eject_features()

#!/usr/bin/bash
venv/bin/pyinstaller --onefile --noconsole --paths src/modules --hidden-import charset_normalizer  --hidden-import PyQt5.QtPrintSupport --workpath target/linux/build --distpath target/linux/dist --specpath target/linux src/main.py

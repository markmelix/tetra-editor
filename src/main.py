import sys

from PyQt5.QtWidgets import QApplication

from core import Core


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Core()
    editor.show()
    sys.exit(app.exec_())

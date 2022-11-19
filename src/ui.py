# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 486)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.global_layout_widget = QtWidgets.QWidget(self.centralwidget)
        self.global_layout_widget.setGeometry(QtCore.QRect(10, 10, 671, 411))
        self.global_layout_widget.setObjectName("global_layout_widget")
        self.global_layout = QtWidgets.QGridLayout(self.global_layout_widget)
        self.global_layout.setContentsMargins(0, 0, 0, 0)
        self.global_layout.setObjectName("global_layout")
        self.tabbar = QtWidgets.QTabWidget(self.global_layout_widget)
        self.tabbar.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabbar.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabbar.setElideMode(QtCore.Qt.ElideNone)
        self.tabbar.setTabsClosable(True)
        self.tabbar.setMovable(True)
        self.tabbar.setTabBarAutoHide(False)
        self.tabbar.setObjectName("tabbar")
        self.global_layout.addWidget(self.tabbar, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        self.file_menu.setObjectName("file_menu")
        self.help_menu = QtWidgets.QMenu(self.menubar)
        self.help_menu.setObjectName("help_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.new_file_action = QtWidgets.QAction(MainWindow)
        self.new_file_action.setObjectName("new_file_action")
        self.save_file_action = QtWidgets.QAction(MainWindow)
        self.save_file_action.setObjectName("save_file_action")
        self.save_file_as_action = QtWidgets.QAction(MainWindow)
        self.save_file_as_action.setObjectName("save_file_as_action")
        self.open_file_action = QtWidgets.QAction(MainWindow)
        self.open_file_action.setObjectName("open_file_action")
        self.settings_action = QtWidgets.QAction(MainWindow)
        self.settings_action.setObjectName("settings_action")
        self.about_action = QtWidgets.QAction(MainWindow)
        self.about_action.setObjectName("about_action")
        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.save_file_action)
        self.file_menu.addAction(self.save_file_as_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.settings_action)
        self.help_menu.addAction(self.about_action)
        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.help_menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabbar.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tetra Code Editor"))
        self.file_menu.setTitle(_translate("MainWindow", "Файл"))
        self.help_menu.setTitle(_translate("MainWindow", "Помощь"))
        self.new_file_action.setText(_translate("MainWindow", "Новый"))
        self.new_file_action.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.save_file_action.setText(_translate("MainWindow", "Сохранить"))
        self.save_file_action.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.save_file_as_action.setText(_translate("MainWindow", "Сохранить как"))
        self.save_file_as_action.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.open_file_action.setText(_translate("MainWindow", "Открыть"))
        self.open_file_action.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.settings_action.setText(_translate("MainWindow", "Настройки"))
        self.settings_action.setShortcut(_translate("MainWindow", "Ctrl+Alt+S"))
        self.about_action.setText(_translate("MainWindow", "О программе"))
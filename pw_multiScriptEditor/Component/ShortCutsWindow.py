# coding=utf8

import os
from Qt import QtCore
from Qt import QtCompat
from Qt import QtWidgets
from load_ui_type import load_ui_type

UI = os.path.join(os.path.dirname(__file__), "shortcutsView.ui")
FormClass, BaseClass = load_ui_type(UI)


class ShortCutsWindow(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(ShortCutsWindow, self).__init__(parent)

        # setup ui
        self.setupUi(self)

        QtCompat.setSectionResizeMode(self.table.horizontalHeader(), QtWidgets.QHeaderView.Stretch)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Action', 'Shortcut'])
        self.read()

    def read(self):
        src = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shortcuts.txt')
        if os.path.exists(src):
            self.label.hide()
            lines = open(src).readlines()
            for i, l in enumerate(lines):
                self.table.insertRow(self.table.rowCount())
                description, shortcut = l.split('>')
                item = QtWidgets.QTableWidgetItem(description)
                self.table.setItem(i, 0, item)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item = QtWidgets.QTableWidgetItem(shortcut)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, 1, item)
        else:
            self.table.hide()

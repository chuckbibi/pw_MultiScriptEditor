# coding=utf8

import os
from Qt import QtCore

from utils.load_ui_type import load_ui_type

UI = os.path.join(os.path.dirname(__file__), "searchWidget.ui")
FormClass, BaseClass = load_ui_type(UI)


class SearchWindow(FormClass, BaseClass):
    searchSignal = QtCore.Signal(str)
    replaceSignal = QtCore.Signal(list)
    replaceAllSignal = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(SearchWindow, self).__init__(parent)

        # setup ui
        self.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Tool)
        center = parent.parent().mapToGlobal(parent.geometry().center())
        myGeo = self.geometry()
        myGeo.moveCenter(center)
        self.setGeometry(myGeo)
        self.find_le.setFocus()
        # connect
        self.find_btn.clicked.connect(self.search)
        self.find_le.returnPressed.connect(self.search)
        self.replace_btn.clicked.connect(self.replace)
        self.replace_le.returnPressed.connect(self.replace)
        self.replaceAll_btn.clicked.connect(self.replaceAll)

    def search(self):
        self.searchSignal.emit(self.find_le.text())
        QtCore.QTimer.singleShot(10, self.find_le.setFocus)

    def replace(self):
        find = self.find_le.text()
        rep = self.replace_le.text()
        self.replaceSignal.emit([find, rep])
        QtCore.QTimer.singleShot(10, self.replace_le.setFocus)

    def replaceAll(self):
        find = self.find_le.text()
        rep = self.replace_le.text()
        self.replaceAllSignal.emit([find, rep])
        QtCore.QTimer.singleShot(10, self.replace_le.setFocus)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        super(findWidgetClass, self).keyPressEvent(event)

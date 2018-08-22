# coding=utf8

import os
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

from LineBarWidget import LineBarWidget
from InputWindow import InputWindow

style = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'style', 'completer.qss')
if not os.path.exists(style):
    style = None


class PagingLabelWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(PagingLabelWidget, self).__init__(parent)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.closeTab)
        self.tabBar().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self.openMenu)

        self.newTabButton = QtWidgets.QPushButton(self)
        self.newTabButton.setMaximumWidth(30)
        self.setCornerWidget(self.newTabButton, QtCore.Qt.TopLeftCorner)

        self.newTabButton.setCursor(QtCore.Qt.ArrowCursor)
        self.newTabButton.setText('+')
        self.newTabButton.clicked.connect(self.addNewTab)
        self.newTabButton.setToolTip("Add Tab")
        self.desk = QtWidgets.QApplication.desktop()

        # variables
        self.p = parent
        self.lastSearch = [0, None]

        # connects
        self.currentChanged.connect(self.hideAllCompleters)

    def closeTab(self, i):
        if self.count() > 1:
            if self.getCurrentText(i).strip():
                # if qt == 1:
                if self.yes_no_question('Close this tab without saving?\n' + self.tabText(i)):
                    # if QMessageBox.question(self, 'Close Tab',
                    #                        'Close this tab without saving?\n'+self.tabText(i),
                    #                         self.buttons) == QMessageBox.Yes:
                    self.removeTab(i)
                # else:
                #     if QMessageBox.question(self, 'Close Tab',
                #                            'Close this tab without saving?\n'+self.tabText(i)) == QMessageBox.Yes:
                #         self.removeTab(i)
            else:
                self.removeTab(i)

    def openMenu(self):
        menu = QtWidgets.QMenu(self)
        menu.addAction(QtWidgets.QAction('Rename Current Tab', self, triggered=self.renameTab))
        menu.exec_(QtGui.QCursor.pos())

    def renameTab(self):
        index = self.currentIndex()
        text = self.tabText(index)
        result = QtWidgets.QInputDialog.getText(self, 'New name', 'Enter New Name', text=text)
        if result[1]:
            self.setTabText(index, result[0])

    def currentTabName(self):
        index = self.currentIndex()
        text = self.tabText(index)
        return text

    def addNewTab(self, name='New Tab', text=None):
        cont = container(text, self.p, self.desk)  # , self.completer)
        cont.edit.saveSignal.connect(self.p.saveSession)
        # cont.edit.executeSignal.connect(self.p.executeSelected)
        self.addTab(cont, name)
        cont.edit.moveCursor(QtGui.QTextCursor.Start)
        self.setCurrentIndex(self.count() - 1)
        return cont.edit

    def getTabText(self, i):
        text = self.widget(i).edit.toPlainText()
        return text

    def addToCurrent(self, text):
        i = self.currentIndex()
        self.widget(i).edit.insertPlainText(text)

    def getCurrentSelectedText(self):
        i = self.currentIndex()
        text = self.widget(i).edit.getSelection()
        return text

    def getCurrentText(self, i=None):
        if i is None:
            i = self.currentIndex()
        text = self.widget(i).edit.toPlainText()
        return text

    def setCurrentText(self, text):
        i = self.currentIndex()
        self.widget(i).edit.setPlainText(text)

    def hideAllCompleters(self):
        for i in range(self.count()):
            self.widget(i).edit.completer.hideMe()

    def current(self):
        return self.widget(self.currentIndex()).edit

    ############################## editor commands
    def undo(self):
        self.current().undo()

    def redo(self):
        self.current().redo()

    def cut(self):
        self.current().cut()

    def copy(self):
        self.current().copy()

    def paste(self):
        self.current().paste()

    def search(self, text=None):
        if text:
            if text == self.lastSearch[0]:
                self.lastSearch[1] += 1
            else:
                self.lastSearch = [text, 0]
            self.lastSearch[1] = self.current().selectWord(text, self.lastSearch[1])

    def replace(self, parts):
        find, rep = parts
        self.lastSearch = [find, 0]
        self.lastSearch[1] = self.current().selectWord(find, self.lastSearch[1], rep)
        self.current().selectWord(find, self.lastSearch[1])

    def replaceAll(self, pat):
        find, rep = pat
        text = self.current().toPlainText()
        text = text.replace(find, rep)
        self.current().setPlainText(text)

    def comment(self):
        self.current().commentSelected()

    def yes_no_question(self, question):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setText(question)
        yes_button = msg_box.addButton("Yes", QtWidgets.QMessageBox.YesRole)
        no_button = msg_box.addButton("No", QtWidgets.QMessageBox.NoRole)
        msg_box.exec_()
        return msg_box.clickedButton() == yes_button


class container(QtWidgets.QWidget):
    def __init__(self, text, parent, desk):
        super(container, self).__init__()
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        # input widget
        self.edit = InputWindow(parent, desk)
        self.edit.executeSignal.connect(parent.executeSelected)
        if text:
            self.edit.addText(text)
        # if not context == 'hou':
        # line number
        # if context == 'hou':
        #     import hou
        #     if hou.applicationVersion()[0] > 14:
        hbox.addWidget(self.edit)
        # return
        self.lineNum = LineBarWidget(self.edit, self)
        self.edit.verticalScrollBar().valueChanged.connect(lambda: self.lineNum.update())
        self.edit.inputSignal.connect(lambda: self.lineNum.update())

        hbox.addWidget(self.lineNum)
        hbox.addWidget(self.edit)

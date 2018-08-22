# coding=utf8

import os
from Qt import QtCore
from Qt import QtGui

from utils.load_ui_type import load_ui_type
from utils.get_docs_content import get_docs_content
from utils.get_image_path import get_image_path

UI = os.path.join(os.path.dirname(__file__), "aboutView.ui")
FormClass, BaseClass = load_ui_type(UI)


class AboutWindow(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)

        # setup ui
        self.setupUi(self)

        self.title_lb.setText(self.title_lb.text() + str(parent.ver))
        self.text_link_lb.setText(text)
        self.icon_lb.setPixmap(
            QtGui.QPixmap(get_image_path('pw')).scaled(60, 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.donate_btn.setMinimumHeight(35)
        self.donate_btn.setIconSize(QtCore.QSize(24, 24))
        self.donate_btn.setIcon(QtGui.QIcon(get_image_path('donate')))
        self.donate_btn.clicked.connect(lambda: parent.openLink('donate'))
        self.donate_btn.hide()
        tested_file = get_docs_content('tested.txt')
        if os.path.exists(tested_file):
            out_text = open(tested_file).read()
            self.textBrowser.setPlainText(out_text)


text = '''Paul Winex 2015
Any question or bug report: paulwinex@gmail.com
'''

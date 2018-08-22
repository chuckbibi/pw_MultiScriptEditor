# coding=utf8

from Component.ScriptEditor import ScriptEditor
from Qt import QtWidgets


def main():
    app = QtWidgets.QApplication([])
    window = ScriptEditor()
    window.setWindowStyle()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

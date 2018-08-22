# coding=utf8

import sys
sys.path.append("./pyLibs")
sys.path.append("./Component")
sys.path.append("./Component.widgets")

from ScriptEditor import ScriptEditor
from Qt import QtWidgets


def main():
    app = QtWidgets.QApplication([])
    window = ScriptEditor()
    window.setWindowStyle()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

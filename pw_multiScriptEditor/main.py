# coding=utf8

import os
import sys
cur_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(cur_dir, "pyLibs"))
sys.path.append(os.path.join(cur_dir, "Component"))
sys.path.append(os.path.join(cur_dir, "Component/widgets"))

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

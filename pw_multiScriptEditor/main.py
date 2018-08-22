# coding=utf8

# from scriptEditor import scriptEditorClass
from widgets.scriptEditor import scriptEditorClass
from Qt import QtWidgets


def main():
    app = QtWidgets.QApplication([])
    window = scriptEditorClass()
    window.setWindowStyle()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

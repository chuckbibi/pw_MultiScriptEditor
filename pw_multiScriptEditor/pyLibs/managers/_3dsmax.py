from pyLibs.Qt import QtCore, QtWidgets

from pw_multiScriptEditor import scriptEditor

reload(scriptEditor)
import MaxPlus
q3dsmax = QtWidgets.QApplication.instance()

class MaxDialogEvents(QtCore.QObject):
    def eventFilter(self, obj, event):
        import MaxPlus
        if event.type() == QtCore.QEvent.WindowActivate:
            MaxPlus.CUI.DisableAccelerators()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            MaxPlus.CUI.EnableAccelerators()

        return False

def show():
    se = scriptEditor.scriptEditorClass(parent=MaxPlus.GetQMaxWindow())
    se.installEventFilter(MaxDialogEvents())
    se.runCommand('import MaxPlus')
    se.MaxEventFilter = MaxDialogEvents()
    se.installEventFilter(se.MaxEventFilter)
    se.setWindowStyle()
    se.show()

'''
add rvsupport-plugins to your env into the var

RV_SUPPORT_PATH=$RV_SUPPORT_PATH:/pathto/rvsupport/plugins

make sure the script editor module is in the python path 

PYTHONPATH=$PYTHONPATH:/pathto/pw_multiscriptEditor

'''

import sys
sys.dont_write_bytecode = 1

from rv import rvtypes, qtutils

from pyLibs.Qt import QtWidgets, QtCore

class ScriptEditorRv(rvtypes.MinorMode):
    '''
    this class creates a menu and
    handles the parenting and creation of a dock widget in which the editor then resides
    '''
    def __init__(self):
        rvtypes.MinorMode.__init__(self)

        self.init("scriptEditorRv",
                  None,
                  None,
                  [("Script Editor",
                    [("Show Editor", self.showUi, "", None)
                     ]
                    )]
                  )
        self.NOT_INIT = True


    def showUi(self, event):
        if self.NOT_INIT:
            self.initUi()
            self.NOT_INIT = False
        self.dialog.show()

    def initUi(self):
        from pw_multiScriptEditor import scriptEditor
        self.mainWindow = qtutils.sessionWindow()
        self.widget = scriptEditor.scriptEditorClass()
        self.dialog = QtWidgets.QDockWidget("%s" % self.widget.windowTitle(), self.mainWindow)
        self.mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dialog)
        self.dialog.setWidget(self.widget)

    def activate(self):
        rvtypes.MinorMode.activate(self)

    def deactivate(self):
        rvtypes.MinorMode.deactivate(self)
        self.dialog.hide()

def createMode():
    """
    Required to initialize the module. RV will call this function to create your mode.
    """
    print("Adding ScriptEditor")
    return ScriptEditorRv()

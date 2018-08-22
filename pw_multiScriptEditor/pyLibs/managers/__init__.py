main = __import__('__main__')
import platform


#######  COMPLETERS  ##############################################

# NUKE
def nukeCompleter(*args):
    import _nuke
    return _nuke.completer(*args)

def getNukeContextMenu(*args):
    import _nuke
    reload(_nuke)
    return _nuke.contextMenu(*args)
###################################################################

# HOUDINI
def houdiniCompleter(*args):
    import _houdini
    return _houdini.completer(*args)
def getHoudiniContextMenu(*args):
    import _houdini
    reload(_houdini)
    return _houdini.contextMenu(*args)
def houdiniDropEvent(*args):
    import _houdini
    reload(_houdini)
    return _houdini.wrapDroppedText(*args)
###################################################################

# MAYA
def mayaCompleter(*args):
    import _maya
    reload(_maya)
    return _maya.completer(*args)

def mayaDropEvent(*args):
    import _maya
    return _maya.wrapDroppedText(*args)
def getMayaContextMenu(*args):
    import _maya
    reload(_maya)
    return _maya.contextMenu(*args)
###################################################################


contextCompleters = dict(
    nuke=nukeCompleter,
    hou=houdiniCompleter,
    maya=mayaCompleter
)

contextMenus = dict(
    hou=getHoudiniContextMenu,
    nuke=getNukeContextMenu,
    maya=getMayaContextMenu
)

dropEvents = dict(
    maya=mayaDropEvent,
    hou=houdiniDropEvent
)

autoImport = dict(
    hou='import hou\n',
    nuke='import nuke\n',
    max='import MaxPlus\n'
)
mayaDragTempData = 'maya_temp_drag_empty_Data'

main_parent = None
context = None
if 'hou' in main.__dict__:
    context = 'hou'
    if main.__dict__['hou'].applicationVersion()[0] >= 15:
         main_parent = main.__dict__['hou'].ui.mainQtWindow()
elif 'cmds' in main.__dict__:
    context = 'maya'
elif 'nuke' in main.__dict__:
    context = 'nuke'
elif 'MaxPlus' in main.__dict__:
    context = 'max'




if platform.system().lower() == 'windows':
    _s = 'w'
elif platform.system().lower() == 'darwin':
    _s = 'x'
else:
    _s = 'l'

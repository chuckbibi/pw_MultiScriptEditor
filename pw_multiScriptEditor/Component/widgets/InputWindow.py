# coding=utf8

import re
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

import jedi

import settingsManager
import managers
from Component.pythonSyntax import design
from Component.pythonSyntax import syntaxHighLighter

from CompleteWidget import CompleteListWidget

addEndBracket = True

indentLen = 4
minimumFontSize = 10
escapeButtons = [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter, QtCore.Qt.Key_Left, QtCore.Qt.Key_Right, QtCore.Qt.Key_Home,
                 QtCore.Qt.Key_End, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown, QtCore.Qt.Key_Delete,
                 QtCore.Qt.Key_Insert, QtCore.Qt.Key_Escape]
font_name = 'Lucida Console'


class InputWindow(QtWidgets.QTextEdit):
    executeSignal = QtCore.Signal()
    saveSignal = QtCore.Signal()
    inputSignal = QtCore.Signal()

    def __init__(self, parent, desk=None):

        super(InputWindow, self).__init__(parent)
        self.p = parent
        self.desk = desk
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.document().setDefaultFont(QtGui.QFont(font_name, minimumFontSize, QtGui.QFont.Normal))
        metrics = QtGui.QFontMetrics(self.document().defaultFont())
        self.setTabStopWidth(4 * metrics.width(' '))
        self.setAcceptDrops(True)
        self.fs = 12
        self.completer = CompleteListWidget(parent, self)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.openMenu)
        data = settingsManager.scriptEditorClass().readSettings()
        self.applyHightLighter(data.get('theme'))
        # self.changeFontSize(False)
        self.changeFontSize(True)

    def focusOutEvent(self, event):
        self.saveSignal.emit()
        # self.completer.hideMe()
        QtWidgets.QTextEdit.focusOutEvent(self, event)

    def hideEvent(self, event):
        self.completer.updateCompleteList()
        try:
            QtWidgets.QTextEdit.hideEvent(self, event)
        except:
            pass

    def applyHightLighter(self, theme=None, qss=None):
        self.blockSignals(True)
        colors = None
        if theme or not theme == 'default':
            colors = design.getColors(theme)
            if self.completer:
                self.completer.updateStyle(colors)
        self.hgl = syntaxHighLighter.PythonHighlighterClass(self, colors)
        st = design.editorStyle(theme)
        self.setStyleSheet(st)
        self.blockSignals(False)

    def applyPreviewStyle(self, colors):
        self.blockSignals(True)
        self.hgl = syntaxHighLighter.PythonHighlighterClass(self, colors)
        qss = design.applyColorToEditorStyle(colors)
        self.setStyleSheet(qss)
        self.completer.setStyleSheet(qss)
        self.blockSignals(False)

    def parseText(self):
        if self.completer:
            text = self.toPlainText()
            self.moveCompleter()
            if text:
                tc = self.textCursor()
                context_completer = False
                pos = tc.position()
                if managers.context in managers.contextCompleters:
                    line = text[:pos].split('\n')[-1]
                    comp, extra = managers.contextCompleters[managers.context](line, self.p.namespace)
                    if comp or extra:
                        context_completer = True
                        self.completer.updateCompleteList(comp, extra)
                if not context_completer:
                    if re.match('[a-zA-Z0-9_.]', text[pos - 1]):
                        offs = 0
                        if managers.context in managers.autoImport:
                            autoImp = managers.autoImport.get(managers.context, '')
                            text = autoImp + text
                            offs = len(autoImp.split('\n')) - 1
                        bl = tc.blockNumber() + 1 + offs
                        col = tc.columnNumber()
                        script = jedi.Script(text, bl, col, '')
                        try:
                            # curframe = inspect.currentframe()
                            # print inspect.getouterframes(curframe, 2)[1][3]
                            self.completer.updateCompleteList(script.completions())
                        except:
                            self.completer.updateCompleteList()
                    else:
                        self.completer.updateCompleteList()
            else:
                self.completer.updateCompleteList()

    def moveCompleter(self):
        # self.p.out.showMessage('move')
        rec = self.cursorRect()
        # pt = self.mapToGlobal(QPoint(rec.bottomRight().x(), rec.y()+self.completer.lineHeight))
        pt = self.mapToGlobal(rec.bottomRight())
        y = x = 0
        if self.completer.isVisible() and self.desk:
            currentScreen = self.desk.screenGeometry(self.mapToGlobal(rec.bottomRight()))
            futureCompGeo = self.completer.geometry()
            futureCompGeo.moveTo(pt)
            if not currentScreen.contains(futureCompGeo):
                try:
                    i = currentScreen.intersect(futureCompGeo)
                except:
                    i = currentScreen.intersected(futureCompGeo)
                x = futureCompGeo.width() - i.width()
                y = futureCompGeo.height() + self.completer.lineHeight if (
                                                                                  futureCompGeo.height() - i.height()) > 0 else 0

        pt = self.mapToGlobal(rec.bottomRight()) + QtCore.QPoint(10 - x, -y)
        # if managers.context == 'hou':
        #     print self.mapToParent(self.geometry().topLeft())
        self.completer.move(pt)

    def charBeforeCursor(self, cursor):
        pos = cursor.position()
        if pos:
            text = self.toPlainText()
            return text[pos - 1]

    def getCurrentIndent(self):
        cursor = self.textCursor()
        auto = self.charBeforeCursor(cursor) == ':'
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.KeepAnchor)
        line = cursor.selectedText()
        result = ''
        if line.strip():
            p = r"(^\s*)"
            m = re.search(p, line)
            if m:
                result = m.group(0)
            if auto:
                result += '    '
        return result

    def keyPressEvent(self, event):
        self.inputSignal.emit()
        parse = 0
        # apply complete
        if event.modifiers() == QtCore.Qt.NoModifier and event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
            if self.completer and self.completer.isVisible():
                self.completer.applyCurrentComplete()
                return
            # auto indent
            else:
                add = self.getCurrentIndent()
                if add:
                    QtWidgets.QTextEdit.keyPressEvent(self, event)
                    cursor = self.textCursor()
                    cursor.insertText(add)
                    self.setTextCursor(cursor)
                    return
        # remove 4 spaces
        elif event.modifiers() == QtCore.Qt.NoModifier and event.key() == QtCore.Qt.Key_Backspace:
            cursor = self.textCursor()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine, QtGui.QTextCursor.KeepAnchor)
            line = cursor.selectedText()
            if line:
                p = r"    $"
                m = re.search(p, line)
                if m:
                    cursor.removeSelectedText()
                    line = line[:-3]
                    cursor.insertText(line)
                    self.setTextCursor(cursor)
            parse = 1
        # comment
        elif event.modifiers() == QtCore.Qt.AltModifier and event.key() == QtCore.Qt.Key_Q:
            self.p.tab.comment()
            return
        # execute selected
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() in [QtCore.Qt.Key_Return,
                                                                                QtCore.Qt.Key_Enter]:
            if self.completer:
                self.completer.updateCompleteList()
            self.executeSignal.emit()
            return
        # ignore Shift + Enter
        elif event.modifiers() == QtCore.Qt.ShiftModifier and event.key() in [QtCore.Qt.Key_Return,
                                                                              QtCore.Qt.Key_Enter]:
            return
        # duplicate
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_D:
            self.duplicate()
            self.update()
            return
        # increase indent
        elif event.key() == QtCore.Qt.Key_Tab:
            if self.completer:
                if self.completer.isVisible():
                    self.completer.applyCurrentComplete()
                    return
            if self.textCursor().selection().toPlainText():
                self.selectBlocks()
                self.moveSelected(True)
                return
            else:
                self.insertPlainText(' ' * indentLen)
                return
        # decrease indent
        elif event.key() == QtCore.Qt.Key_Backtab:
            self.selectBlocks()
            self.moveSelected(False)
            if self.completer:
                self.completer.updateCompleteList()
            return
        # close completer
        elif event.key() in escapeButtons:
            if self.completer:
                self.completer.updateCompleteList()
            self.setFocus()
        # go to completer
        elif event.key() == QtCore.Qt.Key_Down or event.key() == QtCore.Qt.Key_Up:
            if self.completer.isVisible():
                self.completer.activateCompleter(event.key())
                self.completer.setFocus()
                return
        # just close completer
        elif not event.modifiers() == QtCore.Qt.NoModifier and not event.modifiers() == QtCore.Qt.ShiftModifier:
            self.completer.updateCompleteList()
        else:
            parse = 1

        QtWidgets.QTextEdit.keyPressEvent(self, event)
        # start parse text
        if parse and event.text():
            self.parseText()

    def moveSelected(self, inc):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.document().documentLayout().blockSignals(True)
            self.selectBlocks()
            start, end = cursor.selectionStart(), cursor.selectionEnd()
            text = cursor.selection().toPlainText()
            cursor.removeSelectedText()
            if inc:
                newText = self.addTabs(text)
            else:
                newText = self.removeTabs(text)
            cursor.beginEditBlock()
            cursor.insertText(newText)
            cursor.endEditBlock()
            newEnd = cursor.position()
            cursor.setPosition(start)
            cursor.setPosition(newEnd, QtGui.QTextCursor.KeepAnchor)
            self.document().documentLayout().blockSignals(False)
            self.setTextCursor(cursor)
            self.update()

    def commentSelected(self):
        cursor = self.textCursor()
        self.document().documentLayout().blockSignals(True)
        self.selectBlocks()
        pos = cursor.position()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.KeepAnchor)
        text = cursor.selection().toPlainText()
        self.document().documentLayout().blockSignals(False)
        # cursor.removeSelectedText()
        text, offset = self.addRemoveComments(text)
        cursor.insertText(text)
        cursor.setPosition(min(pos + offset, len(self.toPlainText())))
        self.setTextCursor(cursor)
        self.update()

    def addRemoveComments(self, text):
        result = text
        ofs = 0
        if text.strip():
            lines = text.split('\n')
            ind = 0
            while not lines[ind].strip():
                ind += 1
            if lines[ind].strip()[0] == '#':  # remove comment
                result = '\n'.join([x.replace('#', '', 1) for x in lines])
                ofs = -1
            else:  # add comment
                result = '\n'.join(['#' + x for x in lines])
                ofs = 1
        return result, ofs

    def insertText(self, comp):
        cursor = self.textCursor()
        self.document().documentLayout().blockSignals(True)
        cursor.insertText(comp.complete)
        cursor = self.fixLine(cursor, comp)
        self.document().documentLayout().blockSignals(False)
        self.setTextCursor(cursor)
        self.update()

    def fixLine(self, cursor, comp):
        # self.document().documentLayout().blockSignals(True)
        pos = cursor.position()
        linePos = cursor.positionInBlock()

        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.KeepAnchor)
        line = cursor.selectedText()
        cursor.removeSelectedText()

        start = line[:linePos]
        end = line[linePos:]
        before = start[:-len(comp.name)]
        br = ''
        ofs = 0
        if hasattr(comp, 'end_char'):
            if addEndBracket and before and comp.end_char:
                brackets = {'"': '"', "'": "'"}  # , '(':')', '[':']'}
                if before[-1] in brackets:
                    ofs = 1
                    br = brackets[before[-1]]
                    if end and end[0] == brackets[before[-1]]:
                        br = ''

        res = before + comp.name + br + end

        # self.document().documentLayout().blockSignals(False)
        cursor.beginEditBlock()
        cursor.insertText(res)
        cursor.endEditBlock()
        cursor.clearSelection()
        cursor.setPosition(pos + ofs, QtGui.QTextCursor.MoveAnchor)
        return cursor

    def duplicate(self):
        self.document().documentLayout().blockSignals(True)
        cursor = self.textCursor()
        if cursor.hasSelection():  # duplicate selected
            sel = cursor.selectedText()
            end = cursor.selectionEnd()
            cursor.setPosition(end)
            cursor.insertText(sel)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)
        else:  # duplicate line
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.KeepAnchor)
            line = cursor.selectedText()
            cursor.clearSelection()
            cursor.insertText('\n' + line)
            self.setTextCursor(cursor)
        self.document().documentLayout().blockSignals(False)

    def removeTabs(self, text):
        lines = text.split('\n')
        new = []
        pat = re.compile("^ .*")
        for line in lines:
            line = line.replace('\t', ' ' * indentLen)
            for _ in range(4):
                if pat.match(line):
                    line = line[1:]
            new.append(line)
        return '\n'.join(new)

    def addTabs(self, text):
        lines = [(' ' * indentLen) + x for x in text.split('\n')]
        return '\n'.join(lines)

    def selectBlocks(self):
        self.document().documentLayout().blockSignals(True)
        cursor = self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)
        self.document().documentLayout().blockSignals(False)

    def getSelection(self):
        cursor = self.textCursor()
        text = cursor.selection().toPlainText()
        return text

    def addText(self, text):
        if self.completer:
            self.completer.updateCompleteList()
        self.blockSignals(True)
        self.append(text)
        self.blockSignals(False)

    ########################### DROP
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        QtWidgets.QTextEdit.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):
        event.acceptProposedAction()
        QtWidgets.QTextEdit.dragMoveEvent(self, event)

    def dragLeaveEvent(self, event):
        event.accept()
        QtWidgets.QTextEdit.dragLeaveEvent(self, event)

    def dropEvent(self, event):
        event.acceptProposedAction()
        if managers.context in managers.dropEvents and event.mimeData().hasText():
            mim = event.mimeData()
            text = mim.text()
            namespace = self.p.namespace
            text = managers.dropEvents[managers.context](namespace, text, event)
            mim.setText(text)
            QtWidgets.QTextEdit.dropEvent(self, event)
        else:
            QtWidgets.QTextEdit.dropEvent(self, event)

    ################################################################

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if self.completer:
                self.completer.updateCompleteList()
            if event.delta() > 0:
                self.changeFontSize(True)
                # self.zoomIn(1)
            else:
                self.changeFontSize(False)
                # self.zoomOut(1)
        # super(InputWindow, self).wheelEvent(event)
        else:
            QtWidgets.QTextEdit.wheelEvent(self, event)

    def changeFontSize(self, up):
        if managers.context == 'hou':
            if up:
                self.fs = min(30, self.fs + 1)
            else:
                self.fs = max(8, self.fs - 1)
            self.setTextEditFontSize(self.fs)
        else:
            f = self.font()
            size = f.pointSize()
            if up:
                size = min(30, size + 1)
            else:
                size = max(8, size - 1)
            f.setPointSize(size)
            f.setFamily(font_name)
            self.setFont(f)

    def setTextEditFontSize(self, size):
        style = self.styleSheet() + '''QTextEdit
    {
        font-size: %spx;
        font-family: %s;
    }''' % (size, font_name)
        self.setStyleSheet(style)

    def insertFromMimeData(self, source):
        text = source.text()
        # text = re.sub(r'[^\x00-\x7F]','?', text)
        self.insertPlainText(text)

    def getFontSize(self):
        s = self.font().pointSize()
        return s

    def setFontSize(self, size):
        if size > minimumFontSize:
            if managers.context == 'hou':
                self.fs = size
                self.setTextEditFontSize(self.fs)
            else:
                f = self.font()
                f.setPointSize(size)
                self.setFont(f)

    def mousePressEvent(self, event):
        self.completer.updateCompleteList()
        # if managers.context == 'hou':
        #     if event.button() == Qt.LeftButton:
        #         super(InputWindow, self).mousePressEvent(event)
        # else:
        QtWidgets.QTextEdit.mousePressEvent(self, event)

    def selectWord(self, pattern, number, replace=None):
        text = self.toPlainText()
        if not pattern in text:
            return number
        cursor = self.textCursor()
        indexis = [(m.start(0), m.end(0)) for m in re.finditer(self.fixRegextSymbols(pattern), text)]
        if number > len(indexis) - 1:
            number = 0
        cursor.setPosition(indexis[number][0])
        cursor.setPosition(indexis[number][1], QtGui.QTextCursor.KeepAnchor)
        if replace:
            cursor.removeSelectedText()
            cursor.insertText(replace)
        self.setTextCursor(cursor)
        self.setFocus()
        return number

    def fixRegextSymbols(self, pattern):
        for s in ['[', ']', '(', ')', '*', '^', '.', ',', '{', '}', '$']:
            pattern = pattern.replace(s, '\\' + s)
        return pattern

    def replaceAll(selfold, new):
        pass

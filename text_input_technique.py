#!/usr/bin/python
# -*- coding: utf-8 -*-

# the script was written by Michael Schmidt und Erik Blank

import sys
from PyQt5 import QtGui, QtCore, QtWidgets

class SuperText(QtWidgets.QTextEdit):
 
    def __init__(self, sentence):
        super(SuperText, self).__init__()
        self.sentence = sentence
        self.completer = QtWidgets.QCompleter(sentence.split())
        self.timer = QtCore.QTime()
        self.started = False
        self.input = ""
        self.autoCompletion = ""
        self.setStartText(sentence)
        self.initUI()
        print("Event,time(ms),content")

    def setStartText(self, text):
        cur = self.textCursor()
        self.startText = f'<h3>{text}</h3><p>(Press "Enter" to start)</p>'
        self.setHtml(self.startText)
        self.setTextCursor(cur)

    def updateUI(self):
        cur = self.textCursor()
        text = ""
        if self.autoCompletion == "":
            text = self.startText + f'<h3>{self.input}</h3>'
        else:
            text = self.startText + f'<h3>{self.input}<span style="color:grey">{self.autoCompletion}</span></h3>'
        self.setHtml(text)
        self.setTextCursor(cur)


    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:  
        self.onStart(e)  
        if self.started:
            self.onKeyPressed(e)

    def onKeyPressed(self, ev):
        self.log("keyPressed", str(self.timer.elapsed()), ev.key())
        # on "remove"
        if ev.key() == 16777219:
            self.input = self.input[:-1]
        # autocomplete on enter
        elif ev.key() == 16777220:
            self.autoComplete()
        else:
            self.input += ev.text()

        # on "space"
        if ev.key() == 32:
            self.onWordTyped()
        # on "dot"
        if ev.key() == 46:
            self.onWordTyped()
            self.onSentenceTyped()
        self.setAutoCompletion() 
        self.updateUI()

    def setAutoCompletion(self):
        if len(self.input.split()) > 0:
            prefix = self.input.split()[-1]
            self.completer.setCompletionPrefix(prefix)
            word = self.completer.currentCompletion()
            if word != "":
                if word[-1] == ".":
                    word = word[:-1]
            self.autoCompletion = word[len(prefix):]

    def autoComplete(self):
        self.input += self.autoCompletion
        self.autoCompletion = ""
        self.updateUI()


    def onWordTyped(self):
        elapsed = self.timer.elapsed()
        word = self.input.split()[-1]
        if word[-1] == ".":
            word = word[:-1]
        self.log("wordTyped", str(elapsed), word)

    def onSentenceTyped(self):
        elapsed = self.timer.elapsed()
        self.log("sentenceTyped", str(elapsed), self.input)
        self.log("testFinished", str(elapsed), self.input)
        sys.exit(1)

        
    def initUI(self):
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle('SuperText')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        self.show()

    def onStart(self, ev):
        if not self.started:
            if ev.key() == 16777220:
                self.started = True
                self.timer.start()

    def log(self, eventType, time, content):
        print(f'{eventType},{time},{content}')
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    super_text = SuperText("An 123 Tagen kamen 1342 Personen.")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

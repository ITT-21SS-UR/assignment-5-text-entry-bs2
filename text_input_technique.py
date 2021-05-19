#!/usr/bin/python
# -*- coding: utf-8 -*-

# the script was written by Erik Blank

"""
This program meassures the speed of text
entry for following events:
    - key pressed
    - word typed
    - sentence typed
    - programm finished
The user can start the program by hitting "enter".
Afterwards the sentence can be typed
and the program stops when the sentence was typed.
Autocompletion is provided by pressing "enter" while typing the word.
"""

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import pandas as pd

FIELDS = ["id", "event", "time(ms)", "content", "mode"]


class SuperText(QtWidgets.QTextEdit):

    def __init__(self, sentence, id):
        super(SuperText, self).__init__()
        self.id = id
        self.df = pd.DataFrame(columns=FIELDS)
        self.sentence = sentence
        # add QCompleter
        self.completer = QtWidgets.QCompleter(sentence.split())
        self.timerKey = QtCore.QTime()
        self.timerWord = QtCore.QTime()
        self.timerSentence = QtCore.QTime()
        self.started = False
        self.input = ""
        self.autoCompletion = ""
        self.setStartText(sentence)
        self.initUI()
        print("Event,time(ms),content")

    def setStartText(self, text):
        cur = self.textCursor()
        self.startText = f"""<p>Type the following
        sentence:</p><h3>{text}</h3><p>You can use
        autocompletion by pressing "Enter"</p>
        <p>(Press "Enter" to start)</p>"""
        self.setHtml(self.startText)
        self.setTextCursor(cur)

    def updateUI(self):
        cur = self.textCursor()
        text = ""
        if self.autoCompletion == "":
            text = self.startText + f'<h3>{self.input}</h3>'
        else:
            # adds the autocompletion suggestion in grey
            text = self.startText + \
                f'<h3>{self.input}<span style="color:grey">{self.autoCompletion}</span></h3>'
        self.setHtml(text)
        self.setTextCursor(cur)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        self.onStart(e)
        if self.started:
            self.onKeyPressed(e)

    def onKeyPressed(self, ev):
        self.log("keyPressed", str(self.timerKey.elapsed()), ev.key())
        self.timerKey.start()
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

    # sets the autocompletion suggest
    def setAutoCompletion(self):
        if len(self.input.split()) > 0:
            prefix = self.input.split()[-1]
            self.completer.setCompletionPrefix(prefix)
            word = self.completer.currentCompletion()
            if word != "":
                # remove dot for last word in sentence
                if word[-1] == ".":
                    word = word[:-1]
            self.autoCompletion = word[len(prefix):]

    # updated the UI if autocompletion is used
    def autoComplete(self):
        self.input += self.autoCompletion
        self.autoCompletion = ""
        self.updateUI()

    def onWordTyped(self):
        elapsed = self.timerWord.elapsed()
        word = self.input.split()[-1]
        if word[-1] == ".":
            word = word[:-1]
        self.log("wordTyped", str(elapsed), word)
        self.timerWord.start()

    def onSentenceTyped(self):
        elapsed = self.timerSentence.elapsed()
        self.log("sentenceTyped", str(elapsed), self.input[1:])
        self.log("testFinished", str(elapsed), self.input[1:])
        self.df = self.df.to_csv(f'./result_1_{self.id}.csv', index=False)
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
                self.timerKey.start()
                self.timerWord.start()
                self.timerSentence.start()

    def log(self, eventType, time, content):
        print(f'{eventType},{time},{content}')
        self.df = self.df.append({
            "id": self.id,
            "event": eventType,
            "time(ms)": time,
            "content": content,
            "mode": 1
        }, ignore_index=True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) != 2:
        print("usage: python3 <scriptname> <userID>")
        sys.exit(1)
    else:
        id = str(sys.argv[1])
    super_text = SuperText("The five boxing wizards jump very quickly.", id)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

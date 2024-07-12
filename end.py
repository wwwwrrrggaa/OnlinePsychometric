# dialog.py

"""Dialog-style application."""
import pickle
import sys

import PySide6.QtWidgets

import main
import pdfbackend


def getanswerfromsave(filename):
    with open(filename, 'rb') as fp:
        return pickle.load(fp)


def savegrades(grades):
    filename = main.getsaveslot() + "\Grade\Grade.txt"
    with open(filename, 'wb') as fp:
        pickle.dump(grades, fp)


def getchapterscore(a, b):
    sum = 0
    for i in range(len(a)):
        if (a[i] == b[i]):
            sum += 1
    return sum


def calculategrades(answerlist, trueanswerlist):
    shuffle = main.getshuffle()
    fieldscore = [0, 0, 0]
    trueanswerlist = [trueanswerlist[i].replace('\\\\', '\\') for i in range(len(trueanswerlist))]
    for k in range(len(answerlist) - 1):
        i = k
        nowlist = getanswerfromsave(answerlist[k])
        truelist = getanswerfromsave(trueanswerlist[i])
        print(nowlist, truelist)
        truelist.reverse()
        nowlist = [int(b) for b in nowlist]
        truelist = [int(b) for b in truelist]
        fieldscore[int(trueanswerlist[i][-5])] += getchapterscore(nowlist, truelist)

    savegrades(fieldscore)
    a, b, c = pdfbackend.givefinalscores([str(i) for i in fieldscore])
    fieldscore.append(a)
    fieldscore.append(b)
    fieldscore.append(c)
    print(fieldscore)
    return fieldscore


class Window(PySide6.QtWidgets.QDialog):
    @staticmethod
    def _on_destroyed(self):
        sys.exit(0)

    def __init__(self, answerlist, trueanswerlist):
        super().__init__(parent=None)
        # self.connect(Window._on_destroyed)
        self.setWindowTitle("End-screen")
        dialogLayout = PySide6.QtWidgets.QVBoxLayout()
        formLayout = PySide6.QtWidgets.QFormLayout()
        self.Box1 = PySide6.QtWidgets.QLabel()
        self.Box2 = PySide6.QtWidgets.QLabel()
        self.Box3 = PySide6.QtWidgets.QLabel()
        self.Box4 = PySide6.QtWidgets.QLabel()
        self.Box5 = PySide6.QtWidgets.QLabel()
        self.Box6 = PySide6.QtWidgets.QLabel()
        sum = calculategrades(answerlist, trueanswerlist)
        self.Box1.setText(str(sum[0]))
        self.Box2.setText(str(sum[1]))
        self.Box3.setText(str(sum[2]))
        self.Box4.setText(str(sum[3]))
        self.Box5.setText(str(sum[4]))
        self.Box6.setText(str(sum[5]))

        formLayout.addRow("חשיבה מילולית-גולמי:", self.Box1)
        formLayout.addRow("חשיבה כמותית-גולמי:", self.Box2)
        formLayout.addRow("אנגלית-גולמי:", self.Box3)
        formLayout.addRow("ציון רב תחומי:", self.Box4)
        formLayout.addRow("ציון כמותי:", self.Box5)
        formLayout.addRow("ציון מילולי:", self.Box6)

        dialogLayout.addLayout(formLayout)
        self.ButtonOk = PySide6.QtWidgets.QPushButton(self.tr("Ok"))
        self.ButtonExit = PySide6.QtWidgets.QPushButton(self.tr("Exit"))
        dialogLayout.addWidget(self.ButtonOk)
        dialogLayout.addWidget(self.ButtonExit)
        self.setLayout(dialogLayout)
        self.ButtonExit.clicked.connect(self._on_destroyed)

# dialog.py

"""Dialog-style application."""
import pickle
import sys

import PySide6.QtGui
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
    errorFormat = '<span style="color:red;">{}</span>'
    correctFormat = '<span style="color:green;">{}</span>'
    sum = 0
    wronguser = []
    wrongcorrect = []
    for i in range(len(a)):
        if (a[i] == b[i]):
            sum += 1
            wronguser.append(str(a[i]))
            wrongcorrect.append(str(a[i]))

        else:
            wronguser.append(errorFormat.format(str(a[i])))
            wrongcorrect.append(correctFormat.format(str(a[i])))
    return sum, wronguser, wrongcorrect


def givechapters(answerlist, trueanswerlist):
    shuffle = main.getsaveslot()
    shuffle = pickle.load(open(shuffle + '\Grade\Order.txt', 'rb'))
    trueanswerlist = [trueanswerlist[i].replace('\\\\', '\\') for i in range(len(trueanswerlist))]
    finalanswerlist = [0 for i in range(len(trueanswerlist))]
    finaltruelist = [0 for i in range(len(trueanswerlist))]
    for k in range(len(answerlist) - 1):
        i = shuffle[k]
        nowlist = getanswerfromsave(answerlist[k])
        truelist = getanswerfromsave(trueanswerlist[i])
        finalanswerlist[int(trueanswerlist[k][-7])] = nowlist
        finaltruelist[int(trueanswerlist[k][-7])] = truelist
    print(finaltruelist)
    return finalanswerlist, finaltruelist


def getimg(saveslot):
    pass


class Window(PySide6.QtWidgets.QDialog):
    @staticmethod
    def _on_destroyed(self):
        sys.exit(0)

    def __init__(self, answerlist, trueanswerlist):
        super().__init__(parent=None)
        # self.connect(Window._on_destroyed)
        self.setWindowTitle("End-screen")
        height = self.height()
        width = self.width()

        dialogLayout = PySide6.QtWidgets.QHBoxLayout()
        formLayout = PySide6.QtWidgets.QFormLayout()
        answerLayout = PySide6.QtWidgets.QFormLayout()

        pic = PySide6.QtWidgets.QLabel()

        self.Box1 = PySide6.QtWidgets.QLabel()
        self.Box2 = PySide6.QtWidgets.QLabel()
        self.Box3 = PySide6.QtWidgets.QLabel()
        self.Box4 = PySide6.QtWidgets.QLabel()
        self.Box5 = PySide6.QtWidgets.QLabel()
        self.Box6 = PySide6.QtWidgets.QLabel()

        self.Box1.setFont(PySide6.QtGui.QFont('Aptos', 16))
        self.Box2.setFont(PySide6.QtGui.QFont('Aptos', 16))
        self.Box3.setFont(PySide6.QtGui.QFont('Aptos', 16))
        self.Box4.setFont(PySide6.QtGui.QFont('Aptos', 16))
        self.Box5.setFont(PySide6.QtGui.QFont('Aptos', 16))
        self.Box6.setFont(PySide6.QtGui.QFont('Aptos', 16))

        a = PySide6.QtWidgets.QLabel()
        b = PySide6.QtWidgets.QLabel()
        c = PySide6.QtWidgets.QLabel()
        d = PySide6.QtWidgets.QLabel()
        e = PySide6.QtWidgets.QLabel()
        f = PySide6.QtWidgets.QLabel()

        a.setText("חשיבה מילולית-גולמי:")
        b.setText("חשיבה כמותית-גולמי:")
        c.setText("אנגלית-גולמי:")
        d.setText("ציון רב תחומי:")
        e.setText("ציון כמותי:")
        f.setText("ציון מילולי:")

        a.setFont(PySide6.QtGui.QFont('Aptos', 16))
        b.setFont(PySide6.QtGui.QFont('Aptos', 16))
        c.setFont(PySide6.QtGui.QFont('Aptos', 16))
        d.setFont(PySide6.QtGui.QFont('Aptos', 16))
        e.setFont(PySide6.QtGui.QFont('Aptos', 16))
        f.setFont(PySide6.QtGui.QFont('Aptos', 16))

        alist, tlist = givechapters(answerlist, trueanswerlist)
        formLayout.addRow(self.Box1, a)
        formLayout.addRow(self.Box2, b)
        formLayout.addRow(self.Box3, c)
        formLayout.addRow(self.Box4, d)
        formLayout.addRow(self.Box5, e)
        formLayout.addRow(self.Box6, f)

        # self.boxes=[]
        mathrawscore = 0
        hebrawscore = 0
        engrawscore = 0
        answerLayout.setSpacing(10)
        for i in range(len(alist)):
            if ('p' in tlist[i]):
                tlist[i].remove('p')
                grade, wronguser, wrongcorrect = getchapterscore(alist[i], tlist[i])
                long = PySide6.QtWidgets.QLabel(str(wrongcorrect))
            else:
                grade, wronguser, wrongcorrect = getchapterscore(alist[i], tlist[i])
                lenchapter = len(alist[i])
                if (lenchapter == 20):
                    mathrawscore += grade
                elif (lenchapter == 22):
                    engrawscore += grade
                elif (lenchapter == 23):
                    hebrawscore += grade
                # hme
                long = PySide6.QtWidgets.QLabel(str(wrongcorrect))
            short = PySide6.QtWidgets.QLabel(str(wronguser))

            shortbox = PySide6.QtWidgets.QLabel()
            longbox = PySide6.QtWidgets.QLabel()
            difbox = PySide6.QtWidgets.QLabel()
            shortbox.setText("פרק 1 תשובות:".replace('1', str(i + 1)))
            longbox.setText("פרק 1 תשובות נכונות:".replace('1', str(i + 1)))
            difbox.setText("פרק 1 טעויות: 57".replace('1', str(i + 1)).replace('57', str(len(alist[i]) - grade)))
            dif = PySide6.QtWidgets.QLabel()

            short.setFont(PySide6.QtGui.QFont('Aptos', 16))
            dif.setFont(PySide6.QtGui.QFont('Aptos', 16))
            long.setFont(PySide6.QtGui.QFont('Aptos', 16))
            shortbox.setFont(PySide6.QtGui.QFont('Aptos', 16))
            difbox.setFont(PySide6.QtGui.QFont('Aptos', 16))
            longbox.setFont(PySide6.QtGui.QFont('Aptos', 16))

            answerLayout.addRow(short, shortbox)
            answerLayout.addRow(dif, difbox)
            answerLayout.addRow(long, longbox)
            answerLayout.addRow(PySide6.QtWidgets.QLabel())
            answerLayout.addRow(PySide6.QtWidgets.QLabel())

        a, b, c = pdfbackend.givefinalscores([str(hebrawscore), str(mathrawscore), str(engrawscore)])

        self.Box1.setText(str(hebrawscore))
        self.Box2.setText(str(mathrawscore))
        self.Box3.setText(str(engrawscore))
        self.Box4.setText(str(a))
        self.Box5.setText(str(b))
        self.Box6.setText(str(c))

        dialogLayout.setSpacing(50)
        dialogLayout.addLayout(answerLayout)
        dialogLayout.addWidget(pic)
        dialogLayout.addLayout(formLayout)
        pic.setPixmap(PySide6.QtGui.QPixmap(main.getsaveslot() + r"\images\answer.png").scaledToHeight(
            self.window().height() * int(2 * 1.414)))
        pic.setAlignment(PySide6.QtGui.Qt.AlignmentFlag.AlignTop)

        # self.ButtonExit = PySide6.QtWidgets.QPushButton(self.tr("Exit"))
        # dialogLayout.addWidget(self.ButtonExit)
        # self.ButtonExit.clicked.connect(self._on_destroyed)

        self.setLayout(dialogLayout)

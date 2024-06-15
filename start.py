# dialog.py
def getsaveslot():
    return r"E:\Storage\Appdata\Saves\save1\\"


def getappdata():
    return r"E:\Storage\Appdata\\"


def getexamsfolder():
    return r"E:\Storage\Appdata\Exams\\"


"""Dialog-style application."""
import os
import sys
import time
import main

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QComboBox,
    QPushButton,
)

timer = "25:00"
exam = ""


def getlanguage():
    path = getexamsfolder()
    listlanguage = []
    for language in os.listdir(path):
        listlanguage.append(language)
    return listlanguage


def getyears(language):
    path = getexamsfolder() + language
    listyear = []
    for year in os.listdir(path):
        listyear.append(year)
    return listyear


def getquarters(language, year):
    path = getexamsfolder() + language + "\\" + year
    listquarter = []
    for quarter in os.listdir(path):
        quarter = quarter[-5]
        listquarter.append(quarter)
    return listquarter


def gettimelimits():
    return ["10:00", "20:00", "25:00", "30:00", "60:00"]


class Window(QDialog):
    def updateyear(self):
        self.Box2.clear()
        self.Box3.clear()
        self.Box2.addItems(getyears(self.Box1.currentText()))

    def updatequarter(self):
        self.Box3.clear()
        self.Box3.addItems(getquarters(self.Box1.currentText(), self.Box2.currentText()))

    @staticmethod
    def _on_destroyed(self):
        global timer, exam
        main.mainapp(exam, timer)

    def Start(self):
        global exam, timer
        exam = r"E:\Storage\Appdata\Exams\\" + self.Box1.currentText() + '\\' + self.Box2.currentText() + '\\' + self.Box1.currentText() + '-' + self.Box2.currentText() + '-' + self.Box3.currentText() + '.pdf'
        if (os.path.isfile(exam)):
            timer = self.Box4.currentText()
            self.close()
        else:
            pass

    def __init__(self):
        super().__init__(parent=None)
        # self.connect(Window._on_destroyed)
        self.setWindowTitle("ChooseExam")
        dialogLayout = QVBoxLayout()
        formLayout = QFormLayout()
        self.Box1 = QComboBox()
        self.Box2 = QComboBox()
        self.Box3 = QComboBox()
        self.Box4 = QComboBox()

        self.Box1.addItems(getlanguage())
        self.Box4.addItems(gettimelimits())
        formLayout.addRow("Language:", self.Box1)
        formLayout.addRow("Year:", self.Box2)
        formLayout.addRow("Quarter:", self.Box3)
        formLayout.addRow("TimeLimit:", self.Box4)
        self.Box1.activated.connect(self.updateyear)
        self.Box2.activated.connect(self.updatequarter)

        dialogLayout.addLayout(formLayout)
        buttons = QDialogButtonBox()
        self.ButtonOk = QPushButton(self.tr("Ok"))
        self.ButtonExit = QPushButton(self.tr("Exit"))
        buttons = [self.ButtonOk, self.ButtonExit]
        dialogLayout.addWidget(self.ButtonOk)
        dialogLayout.addWidget(self.ButtonExit)

        self.setLayout(dialogLayout)

        self.ButtonOk.clicked.connect(self.Start)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
    main.mainapp(exam, timer)

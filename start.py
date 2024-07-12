# dialog.py
appdatafolder = r"C:\Users\Public\Appdata"
examsfolder = r"C:\Users\Public\Appdata\Exams\\"
saveslot = r"C:\Users\Public\Appdata\Saves\save1"
import main


def getsaveslot():
    global saveslot
    return saveslot


def getappdata():
    return appdatafolder


def getexamsfolder(type):
    return r"C:\Users\Public\Appdata\\" + type + '\\'


def updatesaveslot(value):
    global saveslot
    saveslot = value


import os
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton,
)

timer = "25:00"
exam = ""
examtype = 1


def getlanguage():
    # path = getexamsfolder()
    # listlanguage = []
    # for language in os.listdir(path):
    # listlanguage.append(language)
    # return listlanguage
    return []


def getyears(type, language):
    path = getexamsfolder(type) + language
    listyear = []
    for year in os.listdir(path):
        listyear.append(year)
    return listyear


def getquarters(type, language, year):
    path = getexamsfolder(type) + language + "\\" + year
    listquarter = []
    for quarter in os.listdir(path):
        if (len(quarter) == 1):
            quarter = quarter
        else:
            quarter = quarter[-5]
        listquarter.append(quarter)
    return listquarter


def getallslots():
    return os.listdir(getappdata() + '\Saves')


def gettimelimits():
    return ["10:00", "20:00", "25:00", "30:00", "60:00"]


def gettype():
    return ["FullExams", "Exams"]


class Window(QDialog):
    def updateyear(self):
        self.Box2.clear()
        self.Box3.clear()
        self.Box2.addItems(getyears(self.Box0.currentText(), self.Box1.currentText()))

    def updatequarter(self):
        self.Box3.clear()
        self.Box3.addItems(getquarters(self.Box0.currentText(), self.Box1.currentText(), self.Box2.currentText()))

    def updatelanguage(self):
        self.Box1.clear()
        self.Box1.addItems(os.listdir(r"C:\Users\Public\Appdata\\" + self.Box0.currentText()))

    @staticmethod
    def _on_destroyed(self):
        global timer, exam
        main.mainapp(exam, timer)

    def Start(self):
        global exam, timer, saveslot, examtype
        if (self.Box0.currentText() == "Exams"):
            exam = getexamsfolder(
                self.Box0.currentText()) + self.Box1.currentText() + '\\' + self.Box2.currentText() + '\\' + self.Box1.currentText() + '-' + self.Box2.currentText() + '-' + self.Box3.currentText() + '.pdf'
        else:
            exam = getexamsfolder(
                self.Box0.currentText()) + self.Box1.currentText() + '\\' + self.Box2.currentText() + '\\' + self.Box3.currentText()

        if (os.path.isfile(exam)):
            updatesaveslot(self.Box5.currentText())
            timer = self.Box4.currentText()
            self.close()
        elif (os.path.isdir(exam)):
            updatesaveslot(self.Box5.currentText())
            timer = self.Box4.currentText()
            self.close()
            examtype = 2
        else:
            pass

    def __init__(self):
        super().__init__(parent=None)
        # self.connect(Window._on_destroyed)
        self.setWindowTitle("ChooseExam")
        dialogLayout = QVBoxLayout()
        formLayout = QFormLayout()
        self.Box0 = QComboBox()
        self.Box1 = QComboBox()
        self.Box2 = QComboBox()
        self.Box3 = QComboBox()
        self.Box4 = QComboBox()
        self.Box5 = QComboBox()
        self.Box0.addItems(gettype())
        self.Box1.addItems(getlanguage())
        self.Box4.addItems(gettimelimits())
        self.Box5.addItems(getallslots())
        formLayout.addRow("Version:", self.Box0)
        formLayout.addRow("Language:", self.Box1)
        formLayout.addRow("Year:", self.Box2)
        formLayout.addRow("Quarter:", self.Box3)
        formLayout.addRow("TimeLimit:", self.Box4)
        formLayout.addRow("Choose save slot", self.Box5)
        self.Box0.activated.connect(self.updatelanguage)
        self.Box1.activated.connect(self.updateyear)
        self.Box2.activated.connect(self.updatequarter)

        dialogLayout.addLayout(formLayout)
        self.ButtonOk = QPushButton(self.tr("Ok"))
        self.ButtonExit = QPushButton(self.tr("Exit"))
        dialogLayout.addWidget(self.ButtonOk)
        dialogLayout.addWidget(self.ButtonExit)

        self.setLayout(dialogLayout)

        self.ButtonOk.clicked.connect(self.Start)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
    if (examtype == 1):
        main.mainapp(exam, timer, getsaveslot())
    else:
        main.mainfullapp(exam, timer, getsaveslot())

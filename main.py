# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
import pickle
import random
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from PySide6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QVBoxLayout, QComboBox
from PySide6.QtCore import QCoreApplication, QUrl

import end
import pdfbackend
import start
from mainwindow import MainWindow

saveslot = start.getsaveslot()
timelimit = "25:00"
counter = -1
filenames = []
answers = []
examnames = ""
boxofanswers = []
w = ""
filesavelist = []
chapternames = []
trueanswerlist = []
shuffle = [2, 0, 4, 1, 5, 3]
random.shuffle(shuffle)
pickle.dump(shuffle, open(saveslot + "Grade\Order.txt", 'wb'))


def getshuffle():
    global shuffle
    return shuffle


def finishchapter():
    pass
    global w, boxofanswers, counter, filesavelist
    savelist = [boxofanswers[i].currentText() for i in range(len(boxofanswers))]
    filesavelist.append(pdfbackend.saveanswers(savelist, counter))
    w.close()
    # close chapter


def jumpnextchapter():
    global filenames, counter, answers
    finishchapter()
    mainapp('asda', timelimit)
    # answer=answers[counter]
    # examname=filenames[counter]


def givetimelimit():
    global timelimit
    return timelimit


def createanswerwidget(answers):
    layout = QFormLayout()
    boxesofanswer = [0 for i in range(len(answers))]
    for index in range(len(answers)):
        boxesofanswer[index] = QComboBox()
        boxesofanswer[index].addItems(["1", "2", "3", "4"])
        layout.addRow(str(index + 1), boxesofanswer[index])
    return layout, boxesofanswer


def mainapp(exam, timer):
    global timelimit, counter, answers, examnames, w, boxofanswers, chapternames, trueanswerlist
    if (counter == 5):
        finishchapter()
        w = end.Window(filesavelist, trueanswerlist)
        w.show()
    else:
        timelimit = timer
        argument_parser = ArgumentParser(description="PDF Viewer",
                                         formatter_class=RawTextHelpFormatter)
        argument_parser.add_argument("file", help="The file to open",
                                     nargs='?', type=str)
        options = argument_parser.parse_args()
        w = MainWindow()
        w.showMaximized()
        ###end()
        if (counter == -1):
            examnames, answers, chapternames, trueanswerlist = pdfbackend.main(exam)
        counter += 1
        layout, boxofanswers = createanswerwidget(answers[shuffle[counter]])
        w.open(QUrl.fromLocalFile(examnames[shuffle[counter]]))
        w.addanswers(layout)
        QCoreApplication.exec()


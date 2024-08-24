# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
import os
import pickle
from argparse import ArgumentParser, RawTextHelpFormatter

from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtWidgets import QFormLayout, QComboBox

import end
import pdfbackend
from mainwindow import MainWindow

dir=os.path.realpath(__file__).replace("\main.py", "")+"\Data"

timelimit = "25:00"
counter = -1
limit=5
backendfuncs=[pdfbackend.main,pdfbackend.mainfullexam]
backendresumefuncs=[pdfbackend.mainresume,pdfbackend.mainresumefullexam]
backend=[backendfuncs,backendresumefuncs]
filenames = []
answers = []
examnames = ""
boxofanswers = []
w = ""
filesavelist = []
chapternames = []
trueanswerlist = []
shuffle = [2, 0, 4, 1, 5, 3]
saveslot = "ada"


def updatesaveslot(value):
    global saveslot
    saveslot =dir+"\Saves\\" + value


def getsaveslot():
    global saveslot
    return saveslot


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
    global filenames, counter, answers, typeexam
    finishchapter()
    mainapp("asda", timelimit)

    # answer=answers[counter]
    # examname=filenames[counter]


def givetimelimit():
    global timelimit
    return timelimit


def createanswerwidget(answers):
    if "p" in answers:
        minus = 1
    else:
        minus = 0
    layout = QFormLayout()
    boxesofanswer = [0 for i in range(len(answers) - minus)]
    for index in range(len(answers) - minus):
        boxesofanswer[index] = QComboBox()
        boxesofanswer[index].addItems(["1", "2", "3", "4"])
        layout.addRow(str(index + 1), boxesofanswer[index])
    return layout, boxesofanswer


def mainapp(exam, timer, *args):
    global timelimit, counter, answers, examnames, w, boxofanswers, chapternames, trueanswerlist, typeexam, shuffle,limit,backend,limit
    typeexam = 1
    if counter == limit:
        finishchapter()
        w = end.Window(filesavelist, trueanswerlist)
        print("her")
        w.showMaximized()
    else:
        timelimit = timer
        argument_parser = ArgumentParser(
            description="PDF Viewer", formatter_class=RawTextHelpFormatter
        )
        argument_parser.add_argument(
            "file", help="The file to open", nargs="?", type=str
        )
        options = argument_parser.parse_args()
        w = MainWindow()
        w.showMaximized()
        ###end()
        if counter == -1:
            print(args)
            limit=7 if args[0][2]==0 else 5
            saveslot=args[0][0]

            if(args[0][1]==0):
                updatesaveslot(args[0][0])
                examnames, answers, chapternames, trueanswerlist = backend[args[0][1]][args[0][2]](
                    exam, getsaveslot()
                )
                if(args[0][1]==0):
                    with open(getsaveslot() + "\Grade\Order.txt", "wb") as f:
                        pickle.dump([2, 0, 4, 1, 5, 3], f)
            else:
                updatesaveslot(args[0][0])
                examnames, answers, chapternames, trueanswerlist,counter = pdfbackend.mainresume(saveslot)
        counter += 1
        layout, boxofanswers = createanswerwidget(answers[shuffle[counter]])
        w.open(QUrl.fromLocalFile(examnames[shuffle[counter]]))
        w.addanswers(layout)

        QCoreApplication.exec()




#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: score
"""
from lib import *
from config import *

form, base = loadUiType("score.ui")
class ScoreDlg(QDialog, form):
    def __init__(self):
        super(ScoreDlg, self).__init__()
        self.setupUi(self)
        self.twScores.setRowCount(len(conf.scores))
        for i, data in enumerate(conf.scores):
            setup, game_time = data
            size, mines = setup
            w, h = size
            for j, t in enumerate((w, h, mines, game_time)):
                self.twScores.setItem(i, j, QTableWidgetItem(str(t)))


def recordScore(setup, game_time):
    name = inputBox(None, inf="please input your name:")
    if name:
        conf.scores.append((setup, game_time))
        conf.save()
        ScoreDlg().exec_()

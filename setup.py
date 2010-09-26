#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: setup
"""
from lib import *
from config import *

form, base = loadUiType("setup.ui")
class SetupDlg(QDialog, form):
    def __init__(self):
        super(SetupDlg, self).__init__()
        self.setupUi(self)
        self.sbW.setValue(conf.w)
        self.sbH.setValue(conf.h)
        self.sbMines.setValue(conf.mines)

    def accept(self):
        conf.w = self.sbW.value()
        conf.h = self.sbH.value()
        conf.mines = self.sbMines.value()
        conf.save()
        super(SetupDlg, self).accept()

    @pyqtSlot()
    def on_pbSmall_clicked(self):
        self.sbW.setValue(10)
        self.sbH.setValue(10)
        self.sbMines.setValue(10)

    @pyqtSlot()
    def on_pbMiddle_clicked(self):
        self.sbW.setValue(16)
        self.sbH.setValue(16)
        self.sbMines.setValue(40)

    @pyqtSlot()
    def on_pbBig_clicked(self):
        self.sbW.setValue(30)
        self.sbH.setValue(16)
        self.sbMines.setValue(80)

def getSetup():
    if SetupDlg().exec_() != QDialog.Accepted: return
    return (conf.w, conf.h), conf.mines


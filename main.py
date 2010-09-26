#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: main
"""
from lib import *
from game_scene import *
from config import *
import setup, score

class Face(QWidget):
    def __init__(self, scene):
        super(Face, self).__init__()
        self.scene = scene
        self.button = QPushButton("-_-")
        l = QHBoxLayout(self)
        l.setSpacing(0)
        l.addStretch()
        l.addWidget(self.button)
        l.addStretch()

        scene.changeStatus.connect(self.changeStatus)
        self.button.clicked.connect(self.me)

    def me(self):
        self.scene.start()

    def changeStatus(self, status):
        if status == FAIL:
            self.button.setText('>_<')
        elif status == WIN:
            self.button.setText('^o^')
        else:
            self.button.setText('-_-')            

form, base = loadUiType("mainwindow.ui")
class MainWindow(QMainWindow, form):
    def init(self):
        self.setupUi(self)
        self.scene = GameScene()
        self.scene.setMap((conf.w, conf.h), conf.mines)
        self.scene.start()
        self.face = Face(self.scene)
        #status bar
        self.lbFlag = QLabel("0/99")
        self.lbTimer = QLabel("00:00")
        self.statusBar().addWidget(self.lbFlag)
        self.statusBar().addWidget(self.lbTimer)

        self.fullscreen = False
        self.map_size, self.mines = (10, 10), 10

        self.widget = QWidget()
        l = QVBoxLayout(self.widget)
        l.setSpacing(0)
        l.addWidget(self.face, 0)
        l.addWidget(self.scene, 1)
        self.setCentralWidget(self.widget)
        self.startTimer(1000)

        self.scene.changeFlag.connect(self.changeFlag)
        self.scene.changeStatus.connect(self.changeStatus)

    def changeStatus(self, status):
        self.action_Pause.setEnabled(status == RUNNING)

    def changeFlag(self, count, mines):
        self.lbFlag.setText("%02d/%02d" % (count, mines))

    def timerEvent(self, event):
        # show timer
        time = self.scene.getTimer()
        minute = time / 60
        second = time % 60
        self.lbTimer.setText("%02d:%02d" % (minute,second))

    @pyqtSlot()
    def on_actionAbout_Qt_triggered(self):
        return app.aboutQt()

    @pyqtSlot()
    def on_action_New_triggered(self):
        self.scene.start()

    @pyqtSlot()
    def on_action_Pause_triggered(self):
        self.scene.pause()

    @pyqtSlot()
    def on_action_Full_Screen_triggered(self):
        if self.fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.fullscreen = not self.fullscreen

    @pyqtSlot()
    def on_action_Score_triggered(self):
        score.ScoreDlg().exec_()

    @pyqtSlot()
    def on_action_Setup_triggered(self):
        result = setup.getSetup()
        if not result: return
        self.scene.setMap(*result)
        self.scene.start()
        
def main():
    m = MainWindow()
    m.init()
    m.show()
    app.exec_()
    
if __name__=="__main__":
    main()

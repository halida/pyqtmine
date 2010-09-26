#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: game_scene
"""
from lib import *
import score

#game status
START, RUNNING, FAIL, WIN = range(4)

MARGIN = 3

def random_map(size, count):
    mine_map = np.zeros(size, dtype=np.bool)
    x, y = size
    while count > 0:
        rx = random.randint(0, x-1)
        ry = random.randint(0, y-1)
        if not mine_map[rx, ry]:
            count -= 1
            mine_map[rx, ry] = True
    return mine_map

def hint_map(mine_map):
    x, y = mine_map.shape
    hint_map = np.zeros((x+2, y+2), dtype=np.uint8)
    for dx in range(x):
        for dy in range(y):
            if mine_map[dx, dy]:
                for tx in range(3):
                    for ty in range(3):
                        hint_map[dx+tx, dy+ty] += 1
    return hint_map[1:x+1,1:y+1]
    
class GameScene(QWidget):
    changeStatus =  pyqtSignal(int)
    changeFlag = pyqtSignal(int, int)
    def __init__(self):
        super(GameScene, self).__init__()

    def getTimer(self):
        if self.start_time:
            return int(time.time() - self.start_time)
        else:
            return 0

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.open((event.x(), event.y()))
        elif event.button() == Qt.RightButton:
            self.toggleFlag((event.x(), event.y()))

    def setMap(self, size, mines):
        self.setup = size, mines
        self.map_size = size
        self.mines = mines

    def start(self):
        self.setStatus(RUNNING)
        self.mine_map = random_map(self.map_size, self.mines)
        self.hint_map = hint_map(self.mine_map)
        self.flag_map = np.zeros(self.map_size, dtype=np.bool)
        self.open_map = np.zeros(self.map_size, dtype=np.bool)
        self.update()

    def startTimer(self):
        if not self.start_time:
            self.start_time = time.time()

    def setStatus(self, status):
        self.start_time = None
        self.status = status
        self.changeStatus.emit(status)

    def inGame(func):
        """
        check if this game is running
        """
        def new_func(self, *args, **kw):
            if self.status != RUNNING: return
            return func(self, *args, **kw)
        return new_func

    def getPos(self, pos):
        #caculate size
        w = self.width()
        h = self.height()
        x, y = self.map_size
        mx, my, sx, sy = self.caculateSize(w, h, x, y)

        x, y = pos
        if not ((mx<x<w-mx) and (my<y<h-my)): return
        px = (x-mx)/sx
        py = (y-my)/sy
        return px, py

    @inGame
    def toggleFlag(self, pos):
        place = self.getPos(pos)
        if not place: return

        self.startTimer()
        self.flag_map[place] = not self.flag_map[place]
        self.checkWin()
        self.changeFlag.emit(self.flag_map.sum(), self.mines)
        self.update()

    def checkWin(self):
        if ((self.mine_map == self.flag_map).all() and
            (self.mine_map != self.open_map).all()):
            self.win()

    @inGame
    def open(self, pos):
        place = self.getPos(pos)
        if not place: return
        if self.flag_map[place]: return

        self.startTimer()
        if self.mine_map[place]:
            #die..
            self.open_map[place] = True
            self.fail()
        else:
            #open
            self.openLots(place)
            self.checkWin()
            self.update()

    def pause(self):
        pass

    def fail(self):
        self.setStatus(FAIL)
        self.update()

    def win(self):
        t = self.getTimer()
        self.setStatus(WIN)
        self.update()
        score.recordScore(self.setup, t)
            
    def openLots(self, place):
        """open lots of empty mine fields"""
        if self.open_map[place]: return
        self.open_map[place] = True
        w, h = self.map_size
        if self.hint_map[place] == 0:
            x, y = place
            opens = []
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    tx = x+dx
                    ty = y+dy
                    if tx<0: continue
                    if tx>=w:continue
                    if ty<0: continue
                    if ty>=h:continue
                    if tx==x and ty==y: continue
                    self.openLots((tx, ty))

    def caculateSize(self, w, h, x, y):
        if w/float(h) > x/float(y):
            my = 0
            sx = sy = (h - 2*my)/y
            mx = (w - x*sx) / 2
        else:
            mx = 0
            sx = sy = (w - 2*mx)/x
            my = (h - y*sy) / 2

        return mx, my, sx, sy

    def paintEvent(self, event=None):
        #caculate size
        w = self.width()
        h = self.height()
        x, y = self.map_size
        mx, my, sx, sy = self.caculateSize(w, h, x, y)

        p = QPainter(self)
        # draw lines
        for i in range(x+1):
            p.drawLine(mx+i*sx, my, mx+i*sx, my+y*sy)
        for i in range(y+1):
            p.drawLine(mx, my+i*sy, mx+x*sx, my+i*sy)

        # draw opens
        for tx in range(x):
            for ty in range(y):
                if self.open_map[tx, ty]:
                    p.fillRect(mx+tx*sx+1, my+ty*sy+1,
                               sx-2, sy-2, Qt.white)
                    p.drawText(mx+tx*sx+1, my+ty*sy+1,
                               sx-2, sy-2, Qt.AlignCenter,
                               str(self.hint_map[tx, ty]))
                    # draw open mine
                    if self.mine_map[tx, ty]:
                        p.drawText(mx+tx*sx+1, my+ty*sy+1,
                                   sx-2, sy-2, Qt.AlignCenter,
                                   "*")
                else:
                    p.fillRect(mx+tx*sx+1, my+ty*sy+1,
                               sx-2, sy-2, Qt.green)

        # draw mines
        p.setPen(Qt.blue)
        if self.status in (FAIL, WIN):
            for tx in range(x):
                for ty in range(y):
                    if self.mine_map[tx, ty]:
                        p.drawText(mx+tx*sx+1, my+ty*sy+1,
                                   sx-2, sy-2, Qt.AlignCenter,
                                   "@")
                        
        # draw flags
        p.setPen(Qt.red)
        for tx in range(x):
            for ty in range(y):
                if self.flag_map[tx, ty]:
                    p.drawText(mx+tx*sx+1, my+ty*sy+1,
                               sx-2, sy-2, Qt.AlignCenter,
                               "^")

    

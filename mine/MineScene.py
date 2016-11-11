#encoding=utf-8

import GlobalVar
import time
import Menu
import Scene
import curses
import random
import logging
import Label

class MineState:
    NotOpen = 1
    Opened = 2
    Flagged = 4
    def __init__(self):
        self.state = MineState.NotOpen
        self.isMine = False
        self.isDead = False
        self.otherMineCount = 0
    def getAliveDisplay(self):
        if self.state==MineState.NotOpen:
            return u'▨'
        elif self.state==MineState.Opened:
            if self.isMine: return u'☠'
            else: return u'▢①②③④⑤⑥⑦⑧'[self.otherMineCount]
        elif self.state==MineState.Flagged:
            return u'☿'
        else:
            return u'#'
    def display(self):
        if self.isDead:
            if self.state==MineState.NotOpen:
                if self.isMine: return u'☢'
                else: return self.getAliveDisplay()
            elif self.state==MineState.Opened:
                return self.getAliveDisplay()
            elif self.state==MineState.Flagged:
                if self.isMine: return u'√'
                else: return u'×'
            else: assert(False)
        else:
            return self.getAliveDisplay()

class MineScene(Scene.Scene):
    def __init__(self, rows=10, cols=9, mineTotal=9):
        Scene.Scene.__init__(self)
        self.mineTotalCount = mineTotal
        self.rows = rows
        self.cols = cols
        self.displayStartR = (40-4-self.rows)/2+4
        self.displayStartC = (40-self.cols)/2
        self.surface = [[MineState() for i in range(0,self.cols)] for k in range(0,self.rows)]
        self.curR = self.curC = 0
        self.initMineArea = False
        self.startTime = 0
    def _onOnceDraw(self):
        GlobalVar.screen.drawImage(0, 0, 'mineTitle0')
        GlobalVar.screen.drawImage(1, 0, 'mineTitle1')

        for r in xrange(0, self.rows):
            disp = ''.join([m.display() for m in self.surface[r]])
            GlobalVar.screen.drawTextWidth(r+self.displayStartR, self.displayStartC, disp)

        GlobalVar.screen.drawTextWidth(self.curR+self.displayStartR, self.curC*2+self.displayStartC, self.surface[self.curR][self.curC].display(), curses.A_REVERSE)        

        GlobalVar.screen.drawText(2, 0, u'剩余雷数：%d'%(self.getLeftMine()) )

        self.onShowTime(0)
    def onShowTime(self, tick):
        if self.startTime==0:
            GlobalVar.screen.drawText(3, 0, u'任意按键开始...')
        else:
            GlobalVar.screen.drawText(3, 0, u'已用时间：%d'%(time.time()-self.startTime) )
    def checkInitMineAreaExcept(self, row, col):
        if self.initMineArea:
            return
        self.initMineArea = True
        
        self.startTime = time.time()
        GlobalVar.time.addCallback(self.onShowTime, 1)

        cnt = self.mineTotalCount
        while cnt>0:
            r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if r==row and c==col: continue
            if self.surface[r][c].isMine: continue
            self.surface[r][c].isMine = True
            cnt = cnt-1

        for r in xrange(0, self.rows):
            for c in xrange(0, self.cols):
                self.surface[r][c].otherMineCount = self.getSurroundMineCount(r, c)
                # self.surface[r][c].state = MineState.Opened

    def getSurroundMineCount(self, nr, nc):
        ret = 0
        for r in xrange(nr-1, nr+2):
            for c in xrange(nc-1, nc+2):
                if r<0 or r>=self.rows: continue
                if c<0 or c>=self.cols: continue
                if r==nr and c==nc: continue
                if self.surface[r][c].isMine:
                    ret = ret+1
        return ret
    def getLeftMine(self):
        ret = self.mineTotalCount
        for r in xrange(0, self.rows):
            for c in xrange(0, self.cols):
                if self.surface[r][c].state==MineState.Flagged:
                    ret = ret-1
        return ret
    def expand(self, nr, nc):
        m = self.surface[nr][nc]
        if m.isMine: return
        if m.state!=MineState.NotOpen: return
        m.state=MineState.Opened
        if m.otherMineCount!=0: return
        logging.debug('expand:%d:%d'%(nr, nc))
        logging.debug('00s:%d'%(self.surface[0][0].state))
        for r in xrange(nr-1, nr+2):
            for c in xrange(nc-1, nc+2):
                if r<0 or r>=self.rows: continue
                if c<0 or c>=self.cols: continue
                if r==nr and c==nc: continue
                if m.isMine: continue
                self.expand(r, c)
    def _onClean(self):
        self.curR = self.curC = 0
        self.initMineArea = False
        self.surface = [[MineState() for i in range(0,self.cols)] for k in range(0,self.rows)]
        self.removeAllCallback()
        self.startTime = 0
    def removeAllCallback(self):
        GlobalVar.time.removeCallback(self.onShowTime)
    def enterDead(self):
        self.removeAllCallback()
        for r in xrange(0, self.rows):
            for c in xrange(0, self.cols):
                self.surface[r][c].isDead = True
        self.menu = Menu.Menu(self.displayStartR-2, self.displayStartC)
        self.addMenuItem(u'You Dead,Please press', 'r')
    def enterWin(self):
        self.removeAllCallback()
        self.menu = Menu.Menu(self.displayStartR-2, self.displayStartC)
        self.addMenuItem(u'｡◕‿◕｡ You Win.', 'r')

    def checkWin(self):
        hasOpened = 0
        for r in xrange(0, self.rows):
            for c in xrange(0, self.cols):
                m = self.surface[r][c]
                if m.state==MineState.Opened:
                    hasOpened = hasOpened+1
        if hasOpened+self.mineTotalCount==self.rows*self.cols:
            self.enterWin()
    def _onKeyboard(self, key):
        if key==ord('q'):
            GlobalVar.app.popScene()
            return True
        elif key==ord('t'):
            self.enterWin()
        elif key==ord('f'):
            self.checkInitMineAreaExcept(self.curR, self.curC)
            state = self.surface[self.curR][self.curC].state
            if state==MineState.Opened:
                pass
            elif state==MineState.Flagged:
                self.surface[self.curR][self.curC].state = MineState.NotOpen
            elif state==MineState.NotOpen:
                self.surface[self.curR][self.curC].state = MineState.Flagged
        elif key==ord('k') or key==ord(' '):
            self.checkInitMineAreaExcept(self.curR, self.curC)
            m = self.surface[self.curR][self.curC]
            if m.isMine:
                m.state = MineState.Opened
                self.enterDead()
            elif m.state==MineState.NotOpen:
                self.expand(self.curR, self.curC)
                self.checkWin()
        elif key==ord('r'):
            self.onClean()
        elif key==curses.KEY_UP:
            self.curR = self.curR-1
            if self.curR<0: self.curR = self.rows-1
        elif key==curses.KEY_DOWN:
            self.curR = self.curR+1
            if self.curR==self.rows: self.curR = 0
        elif key==curses.KEY_LEFT:
            self.curC = self.curC-1
            if self.curC<0: self.curC = self.cols-1
        elif key==curses.KEY_RIGHT:
            self.curC = self.curC+1
            if self.curC==self.cols: self.curC = 0
        self.onOnceDraw(0)
    def _onMenu(self, item):
        if item['hot']=='r':
            self.onClean()





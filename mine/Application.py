#encoding=utf-8

import threading
import curses
import time
from Queue import Queue
import logging

import locale
locale.setlocale(locale.LC_ALL, '')

import GlobalVar, GameScreen, TimeMgr, GameImage

class AppEvent:
    AppEvent_AppTick = 100
    AppEvent_Keyboard = 101

class Application:
    def __init__(self):
        self.scenes = []
        self.stdscr = None
        self.appNeedRunning = False
        self.uiThread = None
        self.events = Queue()
        self.keyThread = None

        GlobalVar.app = self
        GlobalVar.screen = GameScreen.GameScreen()
        GlobalVar.time = TimeMgr.TimeMgr()
        GlobalVar.image = GameImage.GameImage()

    def initApp(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.resizeterm(40,80)
        self.stdscr.keypad(1)
        self.stdscr.timeout(100)
        GlobalVar.screen.setStdscr(self.stdscr)

        self.appNeedRunning = True
        self.initUIThread()
        self.initKeyboardThread()

    def deinitApp(self):
        self.appNeedRunning = False
        self.uiThread.join()
        self.keyThread.join()
        if self.stdscr:
            self.stdscr.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        self.stdscr = None

    def uiThreadProc(self):
        while self.appNeedRunning:
            time.sleep(0.05)
            self.pushEvent(AppEvent.AppEvent_AppTick, 0.05)
    def initUIThread(self):
        self.uiThread = threading.Thread(target=self.uiThreadProc)
        self.uiThread.start()

    def keyThreadProc(self):
        while self.appNeedRunning:
            ch = self.stdscr.getch()
            if ch==-1:
                pass
            else:
                self.pushEvent(AppEvent.AppEvent_Keyboard, ch)
    def initKeyboardThread(self):
        self.keyThread = threading.Thread(target=self.keyThreadProc)
        self.keyThread.start()

    def pushEvent(self, tid, data):
        self.events.put({
            'id' : tid,
            'data' : data
        })

    def exitApp(self):
        self.appNeedRunning = False

    def run(self):
        try:
            self.initApp()

            while self.appNeedRunning:
                evt = self.events.get()
                self.onDealEvent(evt)
        except:
            raise
        finally:
            # pass
            self.deinitApp()

    def pushScene(self, scene):
        self.scenes.append(scene)
    def replaceScene(self, scene):
        self.popScene()
        self.pushScene(scene)
    def popScene(self):
        self.scenes[-1].onClean()
        self.scenes.pop()
        self.scenes[-1].onActive()


    def onDealEvent(self, event):
        tid = event['id']
        data = event['data']
        if tid==AppEvent.AppEvent_AppTick:
            GlobalVar.time.update(data)
            self.stdscr.refresh()
        elif tid==AppEvent.AppEvent_Keyboard:
            if data==27:
                self.exitApp()
            else:
                self.scenes[-1].onKeyboard(data)



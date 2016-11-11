#encoding=utf-8

import GlobalVar
import time
import Menu

class Scene:
    def __init__(self):
        GlobalVar.time.addCallback(self.onOnceDraw, 0)
        self.menu = None #Menu.Menu(10, 0)
    def onOnceDraw(self, tick):
        GlobalVar.screen.clear()
        self._onOnceDraw()
        if self.menu:
            self.menu.draw()
        return True
    def _onOnceDraw(self):
        pass
    def onMenu(self, item):
        oldMenu = self.menu
        if self._onMenu(item):
            return
        if oldMenu==self.menu:
            self.menu = None
        self.onOnceDraw(0)
    def _onMenu(self, item):
        pass
    def onKeyboard(self, key):
        if key==27:
            GlobalVar.app.exitApp()
        elif self.menu:
            self.menu.onKeyboard(key)
        else:
            self._onKeyboard(key)
    def _onKeyboard(self, key):
        pass
    def addMenuItem(self, text, hot):
        self.menu.addItem(text, hot, self.onMenu)
    def onActive(self):
        self._onActive()
        self.onOnceDraw(0)
    def _onActive(self):
        pass
    def onClean(self):
        self._onClean()
    def _onClean(self):
        pass

# def _onOnceDraw(self):
#     pass
# def _onKeyboard(self, key):
#     pass
# def _onMenu(self, item):
#     pass
# def _onActive(self):
#     pass
# def _onClean(self):
#     pass
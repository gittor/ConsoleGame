#encoding=utf-8

import curses
import GlobalVar

class Menu:
    def __init__(self, r, c):
        self.items = []
        self.r, self.c = r, c
        self.selectedIdx = -1
    def __del__(self):
        pass
        # assert(False)
        # GlobalVar.time.removeCallback(self.onTickCallback)
    def addItem(self, text, hot, callback):
        self.items.append({
            'text' : text,
            'hot' : hot,
            'callback' : callback
        })
    def onKeyboard(self, key):
        for i,it in enumerate(self.items):
            if ord(it['hot']) == key:
                self.selectedIdx = i
                self.draw()
                GlobalVar.time.addCallback(self.onTickCallback, 0.5)
    def onTickCallback(self, tick):
        if self.selectedIdx in range(0, len(self.items)):
            self.items[self.selectedIdx]['callback']( self.items[self.selectedIdx] )
        return True
    def draw(self):
        for i,it in enumerate(self.items):
            if self.selectedIdx>=0:
                if self.selectedIdx==i:
                    GlobalVar.screen.drawText(self.r+i, self.c, '%s(%c)'%(it['text'], it['hot']), curses.A_STANDOUT)
                else:
                    GlobalVar.screen.drawText(self.r+i, self.c, '%s(%c)'%(it['text'], it['hot']))
            else:
                GlobalVar.screen.drawText(self.r+i, self.c, '%s(%c)'%(it['text'], it['hot']))
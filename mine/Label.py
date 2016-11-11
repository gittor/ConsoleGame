#encoding=utf-8

import GlobalVar

class Label:
    def __init__(self):
        self.r = self.c = 0
        self.text = ''
        self.attr = None
    def draw(self):
        GlobalVar.screen.drawText(self.r, self.c, self.text, self.attr)
    def drawWidth(self):
        GlobalVar.screen.drawTextWidth(self.r, self.c, self.text, self.attr)
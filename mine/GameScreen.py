#encoding=utf-8

import GlobalVar

class GameScreen:
    def __init__(self):
        self.stdscr = None
    def setStdscr(self, stdscr):
        self.stdscr = stdscr
    def drawText(self, r, c, text, attr=None):
        # self.stdscr.addstr(0+1, 0, str(r))
        # return
        if attr:
            self.stdscr.addstr(r, c, text.encode('utf-8'), attr)
        else:
            self.stdscr.addstr(r, c, text.encode('utf-8'))
    def drawTextWidth(self, r, c, text, attr=None):
        tmp = [ch+' ' for ch in text]
        text = ''.join(tmp)
        self.drawText(r, c, text, attr)
    def drawImage(self, r, c, imgName):
        img = GlobalVar.image.get(imgName)
        assert(img)
        self.drawText(r, c, img["content"], img.get('attr'))
    def clear(self):
        self.stdscr.clear()
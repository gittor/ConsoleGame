#encoding=utf-8

import GlobalVar
import time
import Menu
import Scene
import MineScene
import SettingScene

class StartScene(Scene.Scene):
    def __init__(self):
        Scene.Scene.__init__(self)
        self._onActive()
    def _onOnceDraw(self):
        GlobalVar.screen.drawImage(0, 0, 'StartTitle')
        pass
    def _onKeyboard(self, key):
        pass
    def _onMenu(self, item):
        if item['hot']=='q':
            GlobalVar.app.exitApp()
        elif item['hot']=='s':
            GlobalVar.app.pushScene(MineScene.MineScene())
        elif item['hot']=='h':
            GlobalVar.app.pushScene(SettingScene.SettingScene())
    def _onActive(self):
        self.menu = Menu.Menu(12, 0)
        self.addMenuItem(u'开始游戏', 's')
        self.addMenuItem(u'设置难度', 'h')
        self.addMenuItem(u'退出游戏', 'q')
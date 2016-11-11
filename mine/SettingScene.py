#encoding=utf-8

import Scene
import Menu
import MineScene
import GlobalVar

class SettingScene(Scene.Scene):
    def __init__(self):
        Scene.Scene.__init__(self)
        self.menu = Menu.Menu(12, 10)
        self.addMenuItem(u' 9(行)X10(列)  9颗雷', '1')
        self.addMenuItem(u'16(行)X20(列) 40颗雷', '2')
        self.addMenuItem(u'30(行)X40(列) 60颗雷', '3')
        self.addMenuItem(u'返回主界面', 'q')
    def _onOnceDraw(self):
        pass
    def _onKeyboard(self, key):
        pass
    def _onMenu(self, item):
        if item['hot']=='q':
            GlobalVar.app.popScene()
        else:
            if item['hot']=='1':
                scene = MineScene.MineScene(9, 10, 9)
            elif item['hot']=='2':
                scene = MineScene.MineScene(16, 20, 40)
            elif item['hot']=='3':
                scene = MineScene.MineScene(30, 40, 60)
            GlobalVar.app.replaceScene(scene)
        return True

    def _onActive(self):
        pass
    def _onClean(self):
        pass
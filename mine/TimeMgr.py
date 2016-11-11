#encoding=utf-8

import GlobalVar

class TimeMgr:
    def __init__(self):
        self.queue = {}
        self.added = []
    def update(self, tick):
        # GlobalVar.screen.drawText(15, 0, 'there is %d elements'%(len(self.queue)))
        for k, v in self.queue.items():
            v['escape'] += tick
            needRemove = False
            if v['escape'] >= v['second']:
                needRemove = v['callback']( v['second'] )
                v['escape'] = 0
                if v['times'] > 0: v['times'] -= 1
            if needRemove or v['times']==0:
                self.removeCallback(k)

        for x in self.added:
            if isinstance(x, dict):
                self.queue[ x['callback'] ] = x
            elif x in self.queue:
                del self.queue[x]
        self.added = []

    def addCallback(self, callback, second):
        self.addCallbackTimes(callback, second, -1)
    def addCallbackTimes(self, callback, second, times):
        self.added.append({
            'callback' : callback,
            'times' : times,
            'second' : second,
            'escape' : 0
        })
    def removeCallback(self, callback):
        self.added.append(callback)
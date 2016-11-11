#encoding=utf-8

import Application
import StartScene
import logging

##########################
import json
import curses
data = []

content = '                   ♤ ♤ ♤ This is the SweepMine Game! ♤ ♤ ♤                   '
data.append({
    'name' : 'StartTitle',
    'attr' : curses.A_UNDERLINE,
    'content' : content+' '*(80-len(content))
})

data.append({
    'name' : 'mineTitle0',
    'content' : '卍卐'*20
})

content = '重新开始(r)|标记(f)|打开(k)▅ ▆ ▇ 返回(q)'
data.append({
    'name' : 'mineTitle1',
    'attr' : curses.A_UNDERLINE,
    'content' : ' '*(80-len(content))+content
})

fout = open('images.json', 'w')
fout.write(json.dumps(data, indent=4))
fout.close()

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                filename='application.log',
                filemode='w')
#########################

app = Application.Application()
app.pushScene( StartScene.StartScene() )
app.run()

print 'app exited'
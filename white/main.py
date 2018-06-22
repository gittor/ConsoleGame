#encoding=gbk
import pygame
import pygame.locals
import json
from basic import *

import classic, rapid

data = {}
def read_data():
    global data
    try:
        data = json.load( open('data', 'r') )
        #print data
    except Exception as e:
        #print e
        pass
    if 'classic_max' not in data: data['classic_max'] = 0
    if 'rapid_max' not in data: data['rapid_max'] = 0
    
def main():
    pygame.init()
    #pygame.display.init()
    pygame.display.set_caption('do not click white')
    
    
    #win = pygame.display.set_mode( win_size )
    fnt = pygame.font.SysFont('Times New Roman', 36)
    fnt2 = pygame.font.SysFont('Times New Roman', 28)
    
    snd = pygame.mixer.Sound('begin.ogg')
    
    title = ['classic','rapid']
    w = win_size[0]/2
    h = win_size[1]/(len(title)/2)
    
    clock = pygame.time.Clock()
    
    read_data()
    
    running = True
    while running:
        #
        for evt in pygame.event.get():
            if evt.type==pygame.QUIT:
                running = False
                #print 'quit'
            elif evt.type==pygame.locals.KEYDOWN:
                if evt.key==pygame.locals.K_ESCAPE:
                    running = False
            elif evt.type==pygame.locals.MOUSEBUTTONDOWN:
                if evt.button==1:
                    pos = pygame.mouse.get_pos()
                    idx = pos[1]//h * 2 + pos[0]//w
                    if idx==0:
                        snd.play()
                        classic.main()
                        read_data()
                    elif idx==1:
                        snd.play()
                        rapid.main()
                        read_data()
                    else:
                        raise Exception()
        if not running: break

        win.fill( (255,255,255) )
        
        for i in range(0,len(title)//2):
            for j in range(0,2):
                txt,bg = (255,255,255), (0,0,0)
                if (i*2+j)%2==0:
                    txt,bg = bg,txt
                win.fill(bg, (j*w,i*h,w,h))
                win.blit(fnt.render(title[i*2+j],True,txt),(j*w+30,i*h+200))
        
        win.blit(fnt2.render('max:%d'%data['classic_max'],True,(255,0,0)),(30,400))        
        win.blit(fnt2.render('max:%.3f/s'%data['rapid_max'],True,(255,0,0)),(170,400))

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    
if __name__ == '__main__':
    main()
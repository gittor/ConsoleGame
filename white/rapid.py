#encoding=gbk
import random, json
import pygame
from pygame.locals import *
from basic import *

fnt1 = fnt2 = None
snd1 = snd2 = None
white,black,yellow=(255,255,255),(0,0,0),(255,255,0)
red,gray,blue = (255,0,0),(128,128,128),(0,0,255)
clock = pygame.time.Clock()

speed = 0.000
moved = 0
speedCounter = 0
endCounter = 0
endrc = None
endcolor = None
status = 'pause' #'end','running'
line = []
    
def init():
    global speed,moved,speedCounter,status,line
    global endCounter, fnt1, fnt2, snd1, snd2
    speed = moved = speedCounter = 0
    status = 'pause'
    endCounter = 0
    
    fnt1 = pygame.font.SysFont('Arial',24)
    fnt2 = pygame.font.SysFont('Arial',24)
    
    snd1 = pygame.mixer.Sound('click.ogg')
    snd2 = pygame.mixer.Sound('end.ogg')
    #print snd1, snd2

    line = [ [Block(),Block(),Block(),Block()] for i in range(0,5) ]
    for i in range(0,4):
        line[0][i].pos = [i*Block.width,win_size[1]-Block.height]
        line[0][i].color = yellow
    for i in range(1,5):
        for j in range(0,4):
            line[i][j].pos = [j*Block.width,win_size[1]-(i+1)*Block.height]
            line[i][j].color = white
        line[i][random.randint(0,3)].color = black
        
class Block():
    width = win_size[0]/4
    height = win_size[1]/4
    def __init__(self):
        self.pos = [0,0]
        self.color = [0,0,0]
    def ptIn(self, pt):
        w, h = width, height
        if pt[0] in range(self.pos[0],self.pos[0]+w) and \
            pt[1] in range(self.pos[1],self.pos[1]+h):
            return True
        return False
    def rect(self):
        return [self.pos[0],self.pos[1],self.width,self.height]
def main():
    global moved, speedCounter, speed, status, endCounter, endrc, endcolor
    init()
    running = True
    while running:
        for evt in pygame.event.get():
            if evt.type==pygame.QUIT:
                running = False
            elif evt.type==pygame.locals.KEYDOWN:
                if evt.key==pygame.locals.K_ESCAPE:
                    running = False
            elif evt.type==pygame.locals.MOUSEBUTTONDOWN:
                if evt.button==1:
                    if status=='pause':
                        status = 'running'
                    if status!='running' and endCounter>=30:
                        running = False
                        break
                    if speed==0: speed=5
                    pos = pygame.mouse.get_pos()
                    r,c = (win_size[1]-pos[1]+moved)/Block.height,pos[0]/Block.width
                    r,c = int(r),int(c)
                    #print r,c
                    for i in range(0,r):
                        con = True
                        for j in range(0,4):
                            if line[i][j].color==black:
                                con = False
                                break
                        if not con:   break
                    else:
                        #print 'mk', r, c
                        if line[r][c].color==white:
                            line[r][c].color=red
                            #print 'mk0'
                            status = 'end'
                            endrc = [r,c]
                            endcolor = white
                        else:
                            line[r][c].color=gray
                            snd1.play()
        if not running: break
        
        win.fill((0,255,0))
        
        for r in line:
            for c in r:
                rc = c.rect()
                #print rc,rc[1]
                rc[1] += moved
                win.fill(c.color, rc)
           
        for i in range(0,4):
            pygame.draw.line(win,black,(0,i*Block.height+moved),(win_size[0],i*Block.height+moved),1)
        for j in range(0,4):
            pygame.draw.line(win,black,(j*Block.width,0),(j*Block.width,win_size[1]),1)
        win.blit(fnt2.render('%.3f/s'%speed,True,blue), (win_size[0]/3+10,win_size[1]-40))
        if status=='pause':
            for i in range(0,4):
                if line[1][i].color==black:
                    pos = [line[1][i].pos[0],line[1][i].pos[1]+50]
                    win.blit(fnt1.render('START',True,white),pos)
        elif status=='running':
            moved += speed
            speedCounter += 1
            if speedCounter%100==0: speed+=1
            if moved>=Block.height:
                moved=0
                for i in range(0,4):
                    if line[0][i].color==black: 
                        endrc = [0,i]
                        endcolor = black
                        status='end'
                        break
                else:
                    for i in range(1,5):
                        line[i-1] = line[i]
                        for j in range(0,4):
                            line[i-1][j].pos[1] += Block.height
                    line[4] = [Block() for i in range(0,4)]
                    for i in range(0,4):
                        line[4][i].pos = [i*Block.width,-Block.height]
                        line[4][i].color = white
                    line[4][random.randint(0,3)].color=black

        elif status=='end':
            endCounter += 1
            if endCounter==1:
                snd2.play()
            elif endCounter>=30:
                line[endrc[0]][endrc[1]].color = red
                if endCounter%20<10:
                    win.blit(fnt1.render('click to return',True,red),(85,210))
            elif endCounter%10<5:
                line[endrc[0]][endrc[1]].color = red
            else:
                line[endrc[0]][endrc[1]].color = endcolor
            #print 'end'
        
        pygame.display.flip()
        clock.tick(30)
        
    data = {}
    try:
        data = json.load( open('data', 'r') )
    except Exception as e:
        pass
    if 'rapid_max' not in data: data['rapid_max'] = 0
    if data['rapid_max']<speed:
        data["rapid_max"] = speed
        #print data
    json.dump(data, open('data', 'w'))
       
        
        
        
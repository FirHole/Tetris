import pygame as p # type: ignore
from random import randint
import time
import sys
blocks = []

def draw(block, x=0, y=0, r = -1, COLOR = -1):
    pointlist = {
        'S':[ [[x,y], [x+40,y], [x+80,y], [x+80,y+40], [x+120,y+40], [x+120,y+80], [x+80,y+80], [x+40,y+80], [x+40,y+40], [x+0,y+40]],
             [[x,y], [x+40,y], [x+40,y+40], [x+80,y+40], [x+80,y+80], [x+80,y+120], [x+40,y+120], [x+40,y+80], [x,y+80], [x,y+40]] ],
        }

    if block == 'random':
        keys = list(pointlist.keys())
        block = keys[randint(0,len(keys)-1)]

    if block == 'pl':
        return pointlist
    
    if r == -1:
        global R
        r = randint(0, len(pointlist[block])-1)
        R = r

    if COLOR == -1:
        COLOR = color

    p.draw.polygon(SCREEN, COLOR, pointlist[block][r], 0)
    return block

def update():
    SCREEN.fill((0, 0, 0))
    for i in blocks:
        draw(i[0], i[1], i[2], i[3], i[4])
    draw(Block, x, y, R)
    p.display.flip()

def check(Block):
    colls = []
    for i in draw('pl', x, y)[Block][R]:
        if i[1] == 800:
            return True

        if blocks != []:
            for block in blocks:
                for j in draw('pl', block[1], block[2])[block[0]][block[3]]:
                    #print("IJFIDSHGUSHUG*()", i, j)
                    if i == j:
                        colls.append(i)
                        if len(colls) >= 2:
                            if (colls[0][0]+40 == colls[1][0] or colls[0][0] == colls[1][0]+40) and colls[0][1] == colls[1][1]:
                                return True
                            else:
                                colls.pop(0)

p.init()
SCREEN = p.display.set_mode((400, 800))

#p.draw.lines(SCREEN, (200,200,100), True, [[10,10], [100,10], [100, 100], [10,100]], 1)

x, y, color = 120, 0, (randint(100,255), randint(100,255), randint(100,255))
Block = draw('random', x, y)

Time = time.perf_counter()

while True:
    NewTime = time.perf_counter()
    if NewTime - Time >= 1:
        if check(Block):
            #print("BEFORE:",blocks)
            blocks.append([Block,x,y,R])
            #print(blocks)
            x, y, color = 120, 0, (randint(100,255), randint(100,255), randint(100,255))
            Block = draw('random', x, y)

        else:
            y += 40

        Time = NewTime

    update()

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        if event.type == p.KEYDOWN:
            if event.key == p.K_LEFT:
                x -= 40
            elif event.key == p.K_RIGHT:
                x += 40
            elif event.key == p.K_UP:
                try:
                    draw('pl')[Block][R+1]
                    R += 1
                except:
                    R = 0
            elif event.key == p.K_DOWN:
                while True:
                    y += 40
                    if check(Block):
                        down_pressed = True

                        blocks.append([Block, x, y, R, color])
                        x, y, color = 120, 0, (randint(100,255), randint(100,255), randint(100,255))
                        r = 'random'
                        Block = draw('random', x, y)

                        break
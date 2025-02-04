import pygame as p
import time
import sys


figures = {
    'Z': [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]]}

field = [[0 for _ in range(10)] for _ in range(20)]

def draw(matrix, figure):
    SCREEN.fill((0, 0, 0))

    for y, row in enumerate(matrix):
        for x, obj in enumerate(row):
            if obj == 1:
                Block = p.Rect(x*20, y*20, 20, 20)
                p.draw.rect(SCREEN, (255, 0, 0), Block, 0)

    for y, row in enumerate(figure):
        for x, obj in enumerate(row):
            if obj == 1:
                print(data['y'], data['x'])
                try:
                    if y+data['y'] < 20 and matrix[y+data['y']][x+data['x']] != 1:
                        Block = p.Rect((x+data['x'])*20, (y+data['y'])*20, 20, 20)
                        p.draw.rect(SCREEN, (255, 0, 0), Block, 0)
                    else:
                        print('working')
                        return True
                except:
                    data['x'] -= 1
                    return

p.init()
SCREEN = p.display.set_mode((200, 400))

data = {'figure': figures['Z'],
        'x': 4,
        'y': 0}

Time = time.perf_counter()
while True:
    if draw(field, data['figure']):
        for y, row in enumerate(data['figure']):
            for x, obj in enumerate(row):
                if obj == 1:
                    print(y,data['y'],x,data['x'])
                    field[y+data['y']-1][x+data['x']] = 1

        data = {'figure': figures['Z'],
        'x': 4,
        'y': 0}

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        if event.type == p.KEYDOWN:
            if event.key == p.K_LEFT:
                if data['x'] > 0:
                    data['x'] -= 1
            elif event.key == p.K_RIGHT:
                data['x'] += 1
            elif event.key == p.K_UP:
                data['figure'] = tuple(zip(*data['figure'][::-1]))
            elif event.key == p.K_DOWN:
                pass
    
    NewTime = time.perf_counter()
    if NewTime - Time >= 0.5:
        #if check():
        #    spawn()
        #else:
        data['y'] += 1

        Time = NewTime
    p.display.flip()

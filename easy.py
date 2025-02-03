import pygame as p
import sys
from time import sleep

figures = {
    'Z': [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]]}

def draw():
    SCREEN.fill((0, 0, 0))
    for y, row in enumerate(data['figure']):
        for x, obj in enumerate(row):
            if obj == 1:
                Block = p.Rect(x*40+data['x'], y*40+data['y'], 40, 40)
                p.draw.rect(SCREEN, (255, 0, 0), Block, 0)

p.init()
SCREEN = p.display.set_mode((400, 800))

data = {'figure': figures['Z'],
        'x': 120,
        'y': 0}

while True:
    #draw(data['figure'])
    draw()

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        if event.type == p.KEYDOWN:
            if event.key == p.K_LEFT:
                data['x'] -= 40 
            elif event.key == p.K_RIGHT:
                data['x'] += 40
            elif event.key == p.K_UP:
                data['figure'] = tuple(zip(*data['figure'][::-1]))
            elif event.key == p.K_DOWN:
                pass

    p.display.flip()
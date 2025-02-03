import pygame as p
from random import randint
import time
import sys

figures = {
    'Z': [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]]}

'''
figure = figures['Z']

for _ in range(4):
    figure = tuple(zip(*figure[::-1]))
    
    for i in figure:
        print(i)
    print()
'''

def spawn():
    pass

def check():
    pass

def update():
    pass

x, y = 0,0


spawn()

while True:
    NewTime = time.perf_counter()
    if NewTime - Time >= 1:
        if check():
            spawn()
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
                pass
            elif event.key == p.K_DOWN:
              pass
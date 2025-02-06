import pygame as p # type: ignore
from random import randint
import time, sys

Size = 30

figures = {
    'Z': [[1, 1, 0],
          [0, 1, 1]],

    'S': [[0, 1, 1],
          [1, 1, 0]],

    'I': [[1, 1, 1, 1]],

    'L': [[1, 1, 1],
          [1, 0, 0]],

    'J': [[1, 1, 1],
          [0, 0, 1]],

    'T': [[1, 1, 1],
          [0, 1, 0]],

    'O': [[1, 1],
          [1, 1]]

}
keys = list(figures.keys())

field = [[0 for _ in range(10)] for _ in range(20)]


def new_data():
    return {'figure': figures[keys[randint(0, len(keys) - 1)]],
            'x': 4,
            'y': 0,
            'color': (randint(50, 200), randint(50, 200), randint(50, 200))
            }


def game_over():
    p.draw.rect(SCREEN, (100, 100, 100), p.Rect(0, 8.5 * Size, 10 *  Size, Size), 0)
    SCREEN.blit( p.font.SysFont('comicsans', int(Size/2)+3, True).render('Game over! Press Enter to restart', True, (255, 255, 255)), (0, 8.55 * Size))
    p.display.flip()
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    break
        else:
            continue
        break


data = new_data()


def draw(matrix, figure):
    SCREEN.fill((0, 0, 0))

    for x in range(0, Size * 10, Size):
        # print('x:', x)
        p.draw.line(SCREEN, (50, 50, 50), (x, 0), (x, Size * 20), 1)

    p.draw.rect(SCREEN, (100, 100, 100), p.Rect(Size * 10, 0, Size * 20, Size * 20), 0)
    p.draw.rect(SCREEN, (50, 50, 50), p.Rect(Size * 12.5, Size * 2, Size * 5, Size * 4), 0)
    SCREEN.blit( p.font.SysFont('comicsans', Size, True).render('NEXT:', True, (255, 255, 255)), (Size * 13.25, Size * 0.5))

    for y, row in enumerate(matrix):
        for x, obj in enumerate(row):
            if obj:
                Block = p.Rect(x * Size, y * Size, Size, Size)
                p.draw.rect(SCREEN, obj, Block, 0)

    for y, row in enumerate(figure):
        for x, obj in enumerate(row):
            if obj:
                # try:
                a = 0
                try:
                    if y + data['y'] < 20 and matrix[y + data['y']][x + data['x']] == 0:
                        Block = p.Rect((x + data['x']) * Size, (y + data['y']) * Size, Size, Size)
                        p.draw.rect(SCREEN, data['color'], Block, 0)
                    else:
                        return True
                except:
                    data['x'] -= 1
                    print('error')
                    return


p.init()
SCREEN = p.display.set_mode((Size * 20, Size * 20))

Time = time.perf_counter()
move_time = 0.5

while True:
    if draw(field, data['figure']):
        if data['y'] == 0:
            game_over()
            data = new_data()
            move_time = 0.5
            field = [[0 for _ in range(10)] for _ in range(20)]
            continue
        for y, row in enumerate(data['figure']):
            for x, obj in enumerate(row):
                if obj:
                    #print(y, data['y'], x, data['x'])
                    field[y + data['y'] - 1][x + data['x']] = data['color']

        for y, row in enumerate(field):
            blocks = 0
            for x, obj in enumerate(row):
                if obj:
                    blocks += 1
            if blocks == 10:
                field = [[0 for _ in range(10)]] + field[0:y] + field[y + 1:20]
                for i in field:
                    print('DATA:', list((0 if x == 0 else 1) for x in i))
                print(len(field[0]), 'x', len(field))
                move_time *= 0.95
        data = new_data()

    NewTime = time.perf_counter()
    if NewTime - Time >= move_time:
        data['y'] += 1
        print('Cords:', data['x'], data['y'])

        Time = NewTime

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        if event.type == p.KEYDOWN:
            if event.key == p.K_LEFT:
                if data['x'] > 0:
                    data['x'] -= 1
                    for y, row in enumerate(data['figure']):
                        for x, obj in enumerate(row):
                            if field[y + data['y']][x + data['x']] == 1:
                                data['x'] -= 1

            elif event.key == p.K_RIGHT:
                data['x'] += 1
                for y, row in enumerate(data['figure']):
                    for x, obj in enumerate(row):
                        if obj and (x + data['x'] >= 10 or field[y + data['y']][x + data['x']] != 0):
                            data['x'] -= 1

            elif event.key == p.K_UP:
                data['figure'] = tuple(zip(*data['figure'][::-1]))

            elif event.key == p.K_DOWN:
                while True:
                    data['y'] += 1
                    if draw(field, data['figure']):
                        break

            elif event.key == p.K_RETURN:
                p.quit()
                sys.exit()

    p.display.flip()

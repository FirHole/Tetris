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


next_figure = [figures[keys[randint(0, len(keys) - 1)]], (randint(50, 200), randint(50, 200), randint(50, 200))]

def new_data():
    global next_figure
    figure = next_figure.copy()

    while True:
        next_figure = [figures[keys[randint(0, len(keys) - 1)]], (randint(50, 200), randint(50, 200), randint(50, 200))]
        if next_figure[0] != figure[0]:
            break

    return {'figure': figure[0],
            'x': 4,
            'y': 0,
            'color': figure[1],
            'next': next_figure
            }


def message(text):
    p.draw.rect(SCREEN, (100, 100, 100), p.Rect(0, 8.5 * Size, 10 *  Size, Size), 0)
    SCREEN.blit( p.font.SysFont('comicsans', int(Size/2)+3, True).render(text, True, (255, 255, 255)), (0, 8.55 * Size))
    p.display.flip()


def game_over():
    message('Game over! Press Enter to restart')
    
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


def update():
    SCREEN.fill((0, 0, 0))
    global hold, level, points, lines_counter

    for x in range(0, Size * 10, Size):
        p.draw.line(SCREEN, (50, 50, 50), (x, 0), (x, Size * 20), 1)

    p.draw.rect(SCREEN, (100, 100, 100), p.Rect(Size * 10, 0, Size * 20, Size * 20), 0)


    SCREEN.blit( p.font.SysFont('comicsans', Size, True).render('NEXT:', True, (255, 255, 255)), (Size * 13.3, Size * 0.5))
    p.draw.rect(SCREEN, (50, 50, 50), p.Rect(Size * 12.5, Size * 2, Size * 5, Size * 4), 0)

    for y, row in enumerate(data['next'][0]):
        for x, obj in enumerate(row):
            if obj:
                Block = p.Rect((15 - len(row)/2 + x) * Size, (3 + y + (0.5 if len(data['next'][0]) == 1 else 0)) * Size, Size, Size)
                p.draw.rect(SCREEN, data['next'][1], Block, 0)


    SCREEN.blit( p.font.SysFont('comicsans', Size, True).render('HOLD:', True, (255, 255, 255)), (Size * 13.3, Size * 7))
    p.draw.rect(SCREEN, (50, 50, 50), p.Rect(Size * 12.5, Size * 8.5, Size * 5, Size * 5), 0)

    for y, row in enumerate(hold['figure']):
        for x, obj in enumerate(row):
            if obj:
                Block = p.Rect((15 - len(row)/2 + x) * Size, (11 - len(hold['figure'])/2 + y) * Size, Size, Size)
                p.draw.rect(SCREEN, hold['color'], Block, 0)


    SCREEN.blit( p.font.SysFont('comicsans', Size, True).render('LEVEL ' + str(level), True, (255, 255, 255)), (Size * 13, Size * 16))
    SCREEN.blit( p.font.SysFont('comicsans', Size//2, True).render('Next level in: ' + str(10-lines_counter) + ' lines', True, (255, 255, 255)), (Size * 12.5, Size * 17.1))

    SCREEN.blit( p.font.SysFont('comicsans', Size, True).render('SCORE: ' + str(points), True, (255, 255, 255)), (Size * 12, Size * 18.5))

    for y, row in enumerate(field):
        for x, obj in enumerate(row):
            if obj:
                Block = p.Rect(x * Size, y * Size, Size, Size)
                p.draw.rect(SCREEN, obj, Block, 0)

    for y, row in enumerate(data['figure']):
        for x, obj in enumerate(row):
            if obj:
                a = 0
                try:
                    if y + data['y'] < 20 and field[y + data['y']][x + data['x']] == 0:
                        Block = p.Rect((x + data['x']) * Size, (y + data['y']) * Size, Size, Size)
                        p.draw.rect(SCREEN, data['color'], Block, 0)
                    else:
                        return True
                except:
                    data['x'] -= 1
                    return
    p.display.flip()
                

def exit_button(event):
    button = p.Rect(Size/2, Size/2, Size, Size)
    if button.collidepoint(p.mouse.get_pos()):
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            return True
        SCREEN.blit(p.transform.scale(p.image.load('exit_pressed.png'), (Size, Size)), button)
    else:
        SCREEN.blit(p.transform.scale(p.image.load('exit.png'), (Size, Size)), button)
    p.display.flip()


def custom():
    modes = [p.Rect(Size * 1, Size * 3, Size * 8, Size * 5),  p.Rect(Size * 11, Size * 3, Size * 8, Size * 5)]
    selected_mode = modes[0]
    figures = [p.Rect(Size * 1, Size * 10, Size * 3.75, Size * 3), p.Rect(Size * 5.75, Size * 10, Size * 3.75, Size * 3),  p.Rect(Size * 10.5, Size * 10, Size * 3.75, Size * 3), p.Rect(Size * 15.25, Size * 10, Size * 3.75, Size * 3)]
    play = p.Rect(Size * 6, Size * 15, Size * 8, Size)

    SCREEN.fill((70, 80, 90))
    SCREEN.blit( p.font.SysFont('comicsans', Size*1, True).render('CUSTOM SETTINGS', True, (255, 255, 255)), (Size * 5, Size * 1))
    while True:
        for button, text in zip(modes + figures + [play], [' Default Mode', ' Uncorrectable Mode', '1,2,3minoes', 'Tetrominoes', 'Pentominoes','Hexominoes','           Play']):
                if button.collidepoint(p.mouse.get_pos()):
                    p.draw.rect(SCREEN, (30, 30, 30), button, 0)
                else:
                   p.draw.rect(SCREEN, (50, 50, 50), button, 0)
                font = p.font.SysFont('comicsans', int(Size/1.5), True).render(text, True, (255, 255, 255))
                SCREEN.blit(font, button)

                if selected_mode == button:
                    SCREEN.blit(p.transform.scale(p.image.load('square.png'), (Size * 8, Size * 5)), button)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if exit_button(event):
                return
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                if play.collidepoint(event.pos):
                    return True
                for mode in modes:
                    if mode.collidepoint(event.pos):
                       selected_mode = mode

        p.display.flip()


def menu():
    play_button = p.Rect(Size * 5.5, Size * 10, Size * 8, Size)
    custom_button = p.Rect(Size * 5.5, Size * 12, Size * 8, Size)

    while True:
        SCREEN.fill((100, 100, 100))
        SCREEN.blit( p.font.SysFont('comicsans', Size*2, True).render('TETRIS+', True, (255, 255, 255)), (Size * 5.5, Size * 2))

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    game()
                if custom_button.collidepoint(event.pos):
                    if custom():
                        game()
        for button, text in zip([play_button, custom_button], ['Play', 'Custom Mode (not ready)']):
            if button.collidepoint(p.mouse.get_pos()):
                p.draw.rect(SCREEN, (30, 30, 30), button, 0)
            else:
               p.draw.rect(SCREEN, (50, 50, 50), button, 0)
            font = p.font.SysFont('comicsans', int(Size/1.5), True).render(text, True, (255, 255, 255))
            text_rect = font.get_rect(center = (Size * 9.5, Size * (10.5 + (0 if text == 'Play' else 2))))
            SCREEN.blit(font, text_rect)
        p.display.flip()


def game():
    global hold, level, points, lines_counter, data, field

    data = new_data()
    Time = time.perf_counter()
    move_time = 0.05
    level = 1
    lines_counter = 0
    points = 0
    hold = {'figure': [[]]}

    while True:
        if update():
            if data['y'] == 0:
                game_over()
                data = new_data()
                move_time = 0.05
                level = 1
                lines_counter = 0
                points = 0
                field = [[0 for _ in range(10)] for _ in range(20)]
                continue
            for y, row in enumerate(data['figure']):
                for x, obj in enumerate(row):
                    if obj:
                        #print(y, data['y'], x, data['x'])
                        field[y + data['y'] - 1][x + data['x']] = data['color']

            lines = 0
            for y, row in enumerate(field):
                blocks = 0
                for x, obj in enumerate(row):
                    if obj:
                        blocks += 1
                if blocks == 10:
                    field = [[0 for _ in range(10)]] + field[0:y] + field[y + 1:20]
                    #for i in field:
                    #    print('DATA:', list((0 if x == 0 else 1) for x in i))
                    #print(len(field[0]), 'x', len(field))
                    lines += 1
            
            match lines:
                case 1:
                    points += 40 * level
                case 2:
                    points += 100 * level
                case 3:
                    points += 300 * level
                case 4:
                    points += 1200 * level

            lines_counter += lines
            if lines_counter >= 10:
                level += 1
                lines_counter -= 10
            
            move_time = 0.05
            data = new_data()

        NewTime = time.perf_counter()
        if NewTime - Time >= move_time / (level + 10) * 100:
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

                if event.key == p.K_RIGHT:
                    data['x'] += 1
                    for y, row in enumerate(data['figure']):
                        for x, obj in enumerate(row):
                            if obj and (x + data['x'] >= 10 or field[y + data['y']][x + data['x']] != 0):
                                data['x'] -= 1

                if event.key == p.K_UP:
                    data['figure'] = tuple(zip(*data['figure'][::-1]))

                if event.key == p.K_DOWN:
                    move_time = 0.01
                
                if event.key == p.K_LSHIFT or event.key == p.K_RSHIFT:
                    if hold['figure'] != [[]]:
                        hold['next'] = data['next']
                        hold, data = data, hold
                        hold['x'] = 4
                        hold['y'] = 0
                    else:
                        
                        hold, data = data, new_data()
                        hold['x'] = 4
                        hold['y'] = 0

            if event.type == p.KEYUP:
                if event.key == p.K_DOWN:
                    move_time = 0.05
                if event.key == p.K_ESCAPE:
                    message('      The game is paused')
                    
                    for i in [p.KEYDOWN, p.KEYUP]:
                        while True:
                            for event in p.event.get():
                                if event.type == p.QUIT:
                                    p.quit()
                                    sys.exit()
                                if event.type == i:
                                    if event.key == p.K_ESCAPE:
                                        break
                                if exit_button(event):
                                    return
                            else:
                                continue
                            break
        else:
            continue
        break


p.init()
SCREEN = p.display.set_mode((Size * 20, Size * 20))

while True:
    menu()

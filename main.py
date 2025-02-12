import pygame as p
from random import randint
import time, sys
import figures_loader

size = 30


def new_data():
    global next_figure
    figure = next_figure.copy()

    while True:
        next_figure = [figures[keys[randint(0, len(keys) - 1)]], (randint(50, 200), randint(50, 200), randint(50, 200))]
        if next_figure[0] != figure[0]:
            break

    return {'figure': figure[0],
            'x': (field_size // xm - len(figure[0][0])) // 2,
            'y': ((field_size - len(figure[0])) // 2 if xm == 1 else 0),
            'color': figure[1],
            'next': next_figure
            }


def message(text):
    p.draw.rect(SCREEN, (100, 100, 100), p.Rect(0, 8.5 * size, (20 if gravity else 10) *  size, size), 0)
    SCREEN.blit( p.font.SysFont('comicsans', int(size/2)+3, True).render(text, True, (255, 255, 255)), (0, 8.55 * size))
    p.display.flip()


def game_over():
    message(' Game over! Press Enter to restart')
    exit_button()

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    return
            if exit_button(event):
                return True
        p.display.flip()


def exit_button(event = None):
    button = p.Rect(size/2, size/2, size, size)
    if button.collidepoint(p.mouse.get_pos()) and event:
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            return True
        SCREEN.blit(p.transform.scale(p.image.load('assets/exit_pressed.png'), (size, size)), button)
    else:
        SCREEN.blit(p.transform.scale(p.image.load('assets/exit.png'), (size, size)), button)


def custom():
    modes = [p.Rect(size * 1, size * 2, size * 8, size * 5),  p.Rect(size * 11, size * 2, size * 8, size * 5), p.Rect(size * 1, size * 8, size * 8, size * 5),  p.Rect(size * 11, size * 8, size * 8, size * 5)]
    selected_mode = modes[0]
    pieces = [p.Rect(size * 3.125, size * 14, size * 3.75, size * 3), p.Rect(size * 8.125, size * 14, size * 3.75, size * 3),  p.Rect(size * 13.125, size * 14, size * 3.75, size * 3)]
    selected_pieces = [pieces[1]]
    play = p.Rect(size * 6, size * 18, size * 8, size)

    SCREEN.blit(p.transform.scale(p.image.load('assets/custom_bg.png'), (size*20, size*20)), (0,0))
    SCREEN.blit( p.font.SysFont('comicsans', size*1, True).render('CUSTOM SETTINGS', True, (255, 255, 255)), (size * 5, size * 0.2))

    while True:
        if play.collidepoint(p.mouse.get_pos()) and selected_pieces:
            SCREEN.blit(p.transform.scale(p.image.load('assets/play_custom_pressed.png'), (play[2], play[3])), play)
        else:
            SCREEN.blit(p.transform.scale(p.image.load('assets/play_custom.png'), (play[2], play[3])), play)

        for button, asset in zip(modes + pieces + [play], ['default_mode', 'linear_mode', 'dripping_mode', 'random_mode', '123minoes', '4minoes', '5minoes']):
                if selected_mode == button or button in selected_pieces:
                    SCREEN.blit(p.transform.scale(p.image.load('assets/'+asset+'_selected.jpg'), (button[2], button[3])), button)
                else:
                    SCREEN.blit(p.transform.scale(p.image.load('assets/'+asset+'.jpg'), (button[2], button[3])), button)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if exit_button(event):
                return
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                if play.collidepoint(event.pos) and selected_pieces:
                    indexes = [pieces.index(x) for x in selected_pieces]
                    indexes.sort()
                    return modes.index(selected_mode), indexes
                for mode in modes:
                    if mode.collidepoint(event.pos):
                       selected_mode = mode
                for piece in pieces:
                    if piece.collidepoint(event.pos):
                        if piece in selected_pieces:
                           selected_pieces.pop(selected_pieces.index(piece))
                        else:
                            selected_pieces.append(piece)
        p.display.flip()


def menu():
    play_button = p.Rect(size * 5.5, size * 10, size * 8, size)
    custom_button = p.Rect(size * 5.5, size * 12, size * 8, size)

    while True:
        SCREEN.blit(p.transform.scale(p.image.load('assets/menu_bg.png'), (size*20, size*20)), (0,0))
        SCREEN.blit( p.font.SysFont('comicsans', size*2, True).render('TETRIS+', True, (255, 255, 255)), (size * 5.5, size * 2))
        SCREEN.blit( p.font.SysFont('comicsans', size // 2, True).render('by FirHole', True, (255, 255, 255)), (size * 12, size * 4.5))

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    game()
                    return
                if custom_button.collidepoint(event.pos):
                    settings = custom()
                    if settings:
                        game(settings)
                        return

        for button, asset in zip([play_button, custom_button], ['play', 'modes']):
            if button.collidepoint(p.mouse.get_pos()):
                SCREEN.blit(p.transform.scale(p.image.load('assets/'+asset+'_pressed.png'), (button[2], button[3])), button)
            else:
               SCREEN.blit(p.transform.scale(p.image.load('assets/'+asset+'.png'), (button[2], button[3])), button)
        p.display.flip()


def update():
    SCREEN.fill((0, 0, 0))
    global hold, level, points, lines_counter

    for x in range(0, size * 20 // xm, block):
        p.draw.line(SCREEN, (50, 50, 50), (x, 0), (x, size * 20), 2)

    p.draw.rect(SCREEN, (100, 100, 100), p.Rect(size * (20 if gravity else 10), 0, size * 20, size * 20), 0)


    SCREEN.blit( p.font.SysFont('comicsans', size, True).render('NEXT:', True, (255, 255, 255)), (size * (23.3 if gravity else 13.3), size * 0.5))
    SCREEN.blit( p.font.SysFont('comicsans', size, True).render('HOLD:', True, (255, 255, 255)), (size *(23.3 if gravity else 13.3), size * 8))

    x = (22.5 if gravity else 12.5)
    for y in [size * 2, size * 9.5]:
        SCREEN.blit(p.transform.scale(bg, (size * 5, size * 5)), (size * x, y))
        p.draw.lines(SCREEN, (50, 50, 50), True, [(size * x, y), (size * (x + 5), y), (size * (x + 5), y + 5 * size), (size * x, y + 5 * size)], 5)

    for y, row in enumerate(data['next'][0]):
        for x, obj in enumerate(row):
            if obj:
                posx, posy = ((25 if gravity else 15) - len(row)/2 + x) * size, (4.5 - len(data['next'][0]) / 2 + y) * size
                piece = p.Rect(posx, posy, size, size)
                p.draw.rect(SCREEN, data['next'][1], piece, 0)
                p.draw.lines(SCREEN, (210, 210, 210), True, [(posx, posy), (posx + size, posy), (posx + size, posy + size),  (posx, posy + size)], 1)

    for y, row in enumerate(hold['figure']):
        for x, obj in enumerate(row):
            if obj:
                posx, posy = ((25 if gravity else 15) - len(row)/2 + x) * size, (12 - len(hold['figure']) / 2 + y) * size
                piece = p.Rect(posx, posy, size, size)
                p.draw.rect(SCREEN, hold['color'], piece, 0)
                p.draw.lines(SCREEN, (210, 210, 210), True, [(posx, posy), (posx + size, posy), (posx + size, posy + size),  (posx, posy + size)], 1)


    SCREEN.blit( p.font.SysFont('comicsans', size, True).render('LEVEL ' + str(level), True, (255, 255, 255)), (size * (23 if gravity else 13), size * 16))
    SCREEN.blit( p.font.SysFont('comicsans', size//2, True).render('Next level in: ' + str(10 - lines_counter) + ' lines', True, (255, 255, 255)), (size * (22.5 if gravity else 12.5), size * 17.2))

    SCREEN.blit( p.font.SysFont('comicsans', size, True).render('SCORE: ' + str(points), True, (255, 255, 255)), (size * (22 if gravity else 12), size * 18.5))

    for y, row in enumerate(field):
        for x, obj in enumerate(row):
            if obj:
                piece = p.Rect(x * block, y * block, block, block)
                p.draw.rect(SCREEN, obj, piece, 0)
                p.draw.lines(SCREEN, (210, 210, 210), True, [(x * block, y * block), (x * block + block, y * block), (x * block + block, y * block + block), (x * block, y * block + block)], 1)

    for y, row in enumerate(data['figure']):
        for x, obj in enumerate(row):
            if obj:
                try:
                    if y + data['y'] < field_size and field[y + data['y']][x + data['x']] == 0:
                        piece = p.Rect((x + data['x']) * block, (y + data['y']) * block, block, block)
                        p.draw.rect(SCREEN, data['color'], piece, 0)
                        p.draw.lines(SCREEN, (210, 210, 210), True, [((x + data['x']) * block, (y + data['y']) * block), ((x + data['x']) * block + block, (y + data['y']) * block), ((x + data['x']) * block + block, (y + data['y']) * block + block), ((x + data['x']) * block, (y + data['y']) * block + block)], 1)
                    else:
                        return True
                except:
                    data['x'] -= 1
                    return

    for ypos in range(data['y'] + 1, field_size + 1):
        for y, row in enumerate(data['figure']):
            for x, obj in enumerate(row):
                if obj:
                    if y + ypos >= field_size or field[y + ypos][x + data['x']]:
                        break
            else:
                continue
            break
        else:
            continue
        break

    for y, row in enumerate(data['figure']):
        for x, obj in enumerate(row):
            if obj:
                piece = p.Rect((x + data['x']) * block, (y + ypos - 1) * block, block, block)
                p.draw.rect(SCREEN, (40, 40, 40), piece, 0)
                p.draw.lines(SCREEN, (70, 70, 70), True, [((x + data['x']) * block, (y + ypos - 1) * block), ((x + data['x']) * block + block, (y + ypos - 1) * block), ((x + data['x']) * block + block, (y + ypos - 1) * block + block), ((x + data['x']) * block, (y + ypos - 1) * block + block)], 1)
                    
    p.display.flip()


def game(settings = [0, [1]]):
    global hold, level, points, lines_counter, data, field, figures, keys, next_figure, block, field_size, bg, gravity, xm

    figures, multiplier = figures_loader.main(settings[1], settings[0])
    block = int(size / multiplier)
    field_size = int(20 * multiplier)
    xm = 2
    gravity = 0
    keys = list(figures.keys())
    next_figure = [figures[keys[randint(0, len(keys) - 1)]], (randint(50, 200), randint(50, 200), randint(50, 200))]

    Time = time.perf_counter()
    move_time = 0.05
    level = 1
    lines_counter = 0
    points = 0
    hold = {'figure': [[]]}
    hold_times = 1
    bg = p.image.load('assets/custom_bg.png')

    if settings[0] == 3:
        gravity = randint(1, 4)
        xm = 1
        p.display.set_mode((size * 30, size * 20))

    field = [[0 for _ in range(field_size // xm)] for _ in range(field_size)]
    data = new_data()

    while True:
        if update():
            if data['y'] == 0:
                if game_over():
                    return
                data = new_data()
                move_time = 0.05
                level = 1
                lines_counter = 0
                points = 0
                field = [[0 for _ in range(field_size // xm)] for _ in range(field_size)]
                continue

            if settings[0] == 2:
                ystop = field_size + 1
            else:
                ystop = data['y']

            for ypos in range(data['y'] - 1, ystop):
                for y, row in enumerate(data['figure']):
                    for x, obj in enumerate(row):
                        if y + ypos >= field_size:
                            break
                        if obj and field[y + ypos][x + data['x']] == 0:
                            field[y + ypos][x + data['x']] = data['color']

            lines = 0
            for y, row in enumerate(field):
                blocks = 0
                for obj in row:
                    if obj:
                        blocks += 1
                if blocks == field_size // xm:
                    field = [[0 for _ in range(field_size // xm)]] + field[0:y] + field[y+1:field_size]
                    lines += 1

            for y in range(0, len(field) - 1):
                if field[y][0] == (30, 30, 40) and field[y+1][0] == (30, 30, 40):
                    field = [[0 for _ in range(field_size // xm)]] + field[0:y] + field[y+1:field_size]


            match lines:
                case 0:
                    pass
                case 1:
                    points += 40 * level
                case 2:
                    points += 100 * level
                case 3:
                    points += 300 * level
                case _:
                    points += 1200 * level

            lines_counter += lines
            if lines_counter >= 10:
                level += 1
                lines_counter -= 10
            
            move_time = 0.05
            data = new_data()
            hold_times = 1

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
                            if obj and (x + data['x'] >= field_size // xm or field[y + data['y']][x + data['x']] != 0):
                                data['x'] -= 1

                if event.key == p.K_UP:
                    data['figure'] = tuple(zip(*data['figure'][::-1]))

                if event.key == p.K_DOWN:
                    move_time = 0.01

                if event.key == p.K_SPACE:
                    move_time = 0
                
                if (event.key == p.K_LSHIFT or event.key == p.K_RSHIFT) and hold_times < 3:
                    if hold['figure'] != [[]]:
                        hold['next'] = data['next']
                        hold, data = data, hold
                    else:
                        hold, data = data, new_data()
                    hold['x'] = 4
                    hold['y'] = 0
                    hold_times += 1

            if event.type == p.KEYUP:
                if event.key == p.K_DOWN:
                    move_time = 0.05
                if event.key == p.K_ESCAPE:
                    message('      The game is paused')
                    
                    for i in [p.KEYDOWN, p.KEYUP]:
                        exit_button()
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
                                p.display.flip()
                                continue
                            break

p.init()

while True:
    SCREEN = p.display.set_mode((size * 20, size * 20))
    print('resized')
    menu()
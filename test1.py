import pygame as pg
import pygame.gfxdraw
import sys

import pygame_widgets
from pygame_widgets.button import Button
from screeninfo import get_monitors


def monitor_size():
    mon = str(*(get_monitors()))[24:41].split()
    width = int(mon[0][:-1])
    height = int(mon[1][7:])
    return width, height


def button(color, rect):
    global clr, holdingclick
    rect = pg.Rect(120 * rect + 52, length_window - 94, 84, 84)
    if pg.mouse.get_pressed()[0] and rect.collidepoint(mousepos) and not holdingclick:
        clr = color
        dirtyrects.append(toolbar)
    else:
        pg.draw.rect(overlay, color, (rect[0] + 4, rect[1] + 4, rect[2] - 8, rect[3] - 8))
        pg.draw.rect(overlay, black, (rect[0] + 4, rect[1] + 4, rect[2] - 8, rect[3] - 8), 3)


def drawing():
    if shape == 'circle':
        pg.draw.circle(latest1, clr, (x, y), r)
    elif shape == 'rectangle':
        pg.draw.rect(latest1, clr, (x - side_1 // 2, y - side_2 // 2, side_1, side_2))
    elif shape == 'triangle':
        pg.draw.polygon(latest1, clr, [(x, y - side_1,), (x, y + side_1), (x + side_1, y)])
    elif shape == 'left90_triangle':
        pg.draw.polygon(latest1, clr, [(x, y - side_1,), (x + side_1, y + side_1), (x - side_1, y + side_1)])
    elif shape == 'left180_triangle':
        pg.draw.polygon(latest1, clr, [(x, y - side_1), (x, y + side_1), (x - side_1, y)])
    elif shape == 'left270_triangle':
        pg.draw.polygon(latest1, clr, [(x, y + side_1,), (x + side_1, y - side_1), (x - side_1, y - side_1)])


def shiftdown():
    for layer in reversed(layers):
        if layer == latest5:
            window.blit(latest5, (0, 0))
        else:
            layers[layers.index(layer)+1].blit(layer, (0, 0))


def shiftup():
    for layer in layers:
        if layer == latest5:
            layer.fill(clear)
        else:
            layer.fill(clear)
            layer.blit(layers[layers.index(layer)+1], (0, 0))


def change_shape_circle():
    global shape
    shape = 'circle'


def change_shape_rectangle():
    global shape
    shape = 'rectangle'


def change_shape_triangle():
    global shape
    shape = 'triangle'


########################################################################################################################
pg.init()
# Settings:
font = pg.font.SysFont('consolas', 30)
monitor = monitor_size()
width_window = monitor[0]
length_window = monitor[1]
dirtyrects = []
# Colors | R | G | B | A |
clear = (0, 0, 0, 0)
white = (255, 255, 255)
gray = (150, 150, 150)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 125, 0)
yellow = (255, 255, 0)
green = (0, 225, 0)
blue = (0, 0, 255)
purple = (150, 0, 150)
colors = [black, white, red, orange, yellow, green, blue, purple]
figure = [1, 2, 3]
numkey = [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8]
# Surfaces:
window = pg.display.set_mode(monitor)
window.fill(white)
overlay = pg.Surface(monitor).convert_alpha()
# Rects:
screen = pg.Rect(0, 0, monitor[0], monitor[1])
toolbar = pg.Rect(0, length_window * 0.823, width_window, width_window * 0.1)
toolbar2 = pg.Rect(width_window * 0.9, 0, width_window * 0.1, length_window)
ongoing = False
undone = 0
maxundone = 0
holdingclick = False
# Drawing static parts of overlay:
overlay.fill(clear)
latest1 = overlay.copy()
latest2 = overlay.copy()
latest3 = overlay.copy()
latest4 = overlay.copy()
latest5 = overlay.copy()
layers = [latest1, latest2, latest3, latest4, latest5]
for layer in layers:
    layer.fill(clear)

pg.draw.rect(overlay, gray, toolbar)
pg.draw.rect(overlay, black, toolbar, 5)
pg.draw.rect(overlay, gray, toolbar2)
pg.draw.rect(overlay, black, toolbar2, 5)

# Drawing number indicators for colors:
for color in colors:
    text = font.render(str(colors.index(color)+1), True, black)
    overlay.blit(text, (120 * colors.index(color) + 86, length_window - 126))
overlaybg = overlay.copy()
# key_function:
locked_x = False
locked_y = False
# shapes:
clr = black
shape = 'rectangle'
r = 25
side_1 = 25
side_2 = 25
rotate_triangle = 0
rotate_triangle2 = 0
# Buttons:
button_circle = Button(window,
                       int(monitor[0] * 0.935),
                       int(monitor[1] * 0.02),
                       int(monitor[0] * 0.057),
                       int(monitor[1] * 0.1),
                       inactiveColour=(200, 50, 0),
                       hoverColour=(150, 0, 0),
                       pressedColour=(0, 200, 20),
                       onClick=change_shape_circle)
button_rectangle = Button(window,
                          int(monitor[0] * 0.935),
                          int(monitor[1] * 0.2),
                          int(monitor[0] * 0.057),
                          int(monitor[1] * 0.1),
                          inactiveColour=(200, 50, 0),
                          hoverColour=(150, 0, 0),
                          pressedColour=(0, 200, 20),
                          onClick=change_shape_rectangle)
button_triangle = Button(window,
                         int(monitor[0] * 0.935),
                         int(monitor[1] * 0.38),
                         int(monitor[0] * 0.057),
                         int(monitor[1] * 0.1),
                         inactiveColour=(200, 50, 0),
                         hoverColour=(150, 0, 0),
                         pressedColour=(0, 200, 20),
                         onClick=change_shape_triangle)
button_locked_x = Button(window,
                         int(monitor[0] * 0.925),
                         int(monitor[1] * 0.84),
                         int(monitor[0] * 0.057),
                         int(monitor[1] * 0.04),
                         text='press x to locked "x"',
                         textColour=red,
                         fontSize=25,
                         inactiveColour=gray,
                         hoverColour=gray,
                         pressedColour=gray)
button_locked_y = Button(window,
                         int(monitor[0] * 0.925),
                         int(monitor[1] * 0.9),
                         int(monitor[0] * 0.057),
                         int(monitor[1] * 0.04),
                         text='press y to locked "y"',
                         textColour=red,
                         fontSize=25,
                         inactiveColour=gray,
                         hoverColour=gray,
                         pressedColour=gray)
########################################################################################################################


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEMOTION:
            mousepos = pg.mouse.get_pos()
            if not locked_x:
                x = mousepos[0]
            if not locked_y:
                y = mousepos[1]
            holdingclick = True
            if screen.collidepoint(mousepos):
                dirtyrects.append(screen)
        if event.type == pg.MOUSEBUTTONDOWN:
            holdingclick = False
            if screen.collidepoint(mousepos):
                dirtyrects.append(screen)
            # Changing brush size:
            if shape == 'circle':
                if event.button == 4 and r < 100:
                    r += 1
                    dirtyrects.append(screen)
                elif event.button == 5 and r > 2:
                    r -= 1
                    dirtyrects.append(screen)
            if shape == 'rectangle':
                if event.button == 4 and side_1 < 100 and side_2 < 100:
                    side_1 += 1
                    side_2 += 1
                    dirtyrects.append(screen)
                elif event.button == 5 and side_1 > 2 and side_2 > 2:
                    side_1 -= 1
                    side_2 -= 1
                    dirtyrects.append(screen)
            if shape == 'triangle':
                if event.button == 4 and side_1 < 100 and side_2 < 100:
                    side_1 += 1
                    dirtyrects.append(screen)
                elif event.button == 5 and side_1 > 2 and side_2 > 2:
                    side_1 -= 1
                    dirtyrects.append(screen)
            if shape == 'left90_triangle':
                if event.button == 4 and side_1 < 100 and side_2 < 100:
                    side_1 += 1
                    dirtyrects.append(screen)
                elif event.button == 5 and side_1 > 2 and side_2 > 2:
                    side_1 -= 1
                    dirtyrects.append(screen)
            if shape == 'left180_triangle':
                if event.button == 4 and side_1 < 100 and side_2 < 100:
                    side_1 += 1
                    dirtyrects.append(screen)
                elif event.button == 5 and side_1 > 2 and side_2 > 2:
                    side_1 -= 1
                    dirtyrects.append(screen)
            if shape == 'left270_triangle':
                if event.button == 4 and side_1 < 100 and side_2 < 100:
                    side_1 += 1
                    dirtyrects.append(screen)
                elif event.button == 5 and side_1 > 2 and side_2 > 2:
                    side_1 -= 1
                    dirtyrects.append(screen)
        if event.type == pg.KEYDOWN:
            if event.key in numkey:
                clr = colors[numkey.index(event.key)]
                dirtyrects.append(toolbar)
            # Emptying canvas:
            if event.key == pg.K_e:
                window.fill(white)
                latest5.fill(clear)
                latest4.fill(clear)
                latest3.fill(clear)
                latest2.fill(clear)
                latest1.fill(clear)
                undone = 0
                maxundone = 0
                dirtyrects.append(screen)
            # Undoing and redoing:
            if event.key == pg.K_u and undone < maxundone:
                undone += 1
                dirtyrects.append(screen)
            if event.key == pg.K_i and undone > 0:
                undone -= 1
                dirtyrects.append(screen)
            if shape == 'triangle':
                if event.key == pygame.K_LEFT:
                    shape = 'left90_triangle'
            if shape == 'left90_triangle' and rotate_triangle >= 1:
                if event.key == pygame.K_RIGHT:
                    shape = 'triangle'
                    rotate_triangle = 0
                if event.key == pygame.K_LEFT:
                    shape = 'left180_triangle'
            if shape == 'left180_triangle' and rotate_triangle2 >= 1:
                if event.key == pygame.K_RIGHT:
                    shape = 'left90_triangle'
                    rotate_triangle2 = 0
                if event.key == pygame.K_LEFT:
                    shape = 'left270_triangle'
            if shape == 'left270_triangle':
                if event.key == pygame.K_RIGHT:
                    shape = 'left180_triangle'
            if event.key == pg.K_x:
                if not locked_x:
                    locked_x = True
                    color_for_locked_x = green
                else:
                    locked_x = False
                    color_for_locked_x = red
                button_locked_x = Button(window,
                                         int(monitor[0] * 0.925),
                                         int(monitor[1] * 0.84),
                                         int(monitor[0] * 0.057),
                                         int(monitor[1] * 0.04),
                                         text='press x to locked "x"',
                                         textColour=color_for_locked_x,
                                         fontSize=25,
                                         inactiveColour=gray,
                                         hoverColour=gray,
                                         pressedColour=gray)
            if event.key == pg.K_y:
                if not locked_y:
                    locked_y = True
                    color_for_locked_y = green
                else:
                    locked_y = False
                    color_for_locked_y = red
                button_locked_y = Button(window,
                                         int(monitor[0] * 0.925),
                                         int(monitor[1] * 0.9),
                                         int(monitor[0] * 0.057),
                                         int(monitor[1] * 0.04),
                                         text='press y to locked "y"',
                                         fontSize=25,
                                         inactiveColour=gray,
                                         hoverColour=gray,
                                         pressedColour=gray)
    # Painting:
    if pg.mouse.get_pressed()[0] and screen.collidepoint(mousepos):
        if not ongoing:
            while undone > 0:
                shiftup()
                undone -= 1
                maxundone -= 1
            shiftdown()
        drawing()
        ongoing = True
    else:
        if ongoing:
            if maxundone < 5:
                maxundone += 1
            ongoing = False
    if screen in dirtyrects:
        # Drawing canvas:
        window.fill(white)
        for layer in layers:
            if layers.index(layer) == undone:
                window.blit(pg.transform.smoothscale(layer, (screen[2], screen[3])), screen)
        # Drawing overlay:
        overlay.fill(clear)
        if shape == 'circle':
            if r > 1:
                pg.gfxdraw.circle(overlay, x, y, r, clr)
        elif shape == 'rectangle':
            pygame.gfxdraw.rectangle(overlay,
                                     (x - side_1 // 2, y - side_2 // 2, side_1, side_2), clr)
        elif shape == 'triangle':
            pygame.gfxdraw.polygon(overlay,
                                   [(x, y - side_1,), (x, y + side_1),
                                    (x + side_1, y)], clr)
        elif shape == 'left90_triangle':
            rotate_triangle += 1
            pygame.gfxdraw.polygon(overlay,
                                   [(x, y - side_1),
                                    (x + side_1, y + side_1),
                                    (x - side_1, y + side_1)], clr)
        elif shape == 'left180_triangle':
            rotate_triangle2 += 1
            pygame.gfxdraw.polygon(overlay, [(x, y - side_1),
                                             (x, y + side_1),
                                             (x - side_1, y)], clr)
        elif shape == 'left270_triangle':

            pygame.gfxdraw.polygon(overlay, [(x, y + side_1),
                                             (x + side_1, y - side_1),
                                             (x - side_1, y - side_1)], clr)
    overlay.blit(overlaybg, screen)
    for color in colors:
        button(color, colors.index(color))
    window.blit(overlay, screen)
    # Updating display:
    pygame_widgets.update(event)
    pg.display.update()
    pg.display.update(dirtyrects)
    dirtyrects.clear()

import pygame as pg
import pygame.gfxdraw
import sys
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from screeninfo import get_monitors
from PIL import Image
import pygame_menu
import sqlite3
import os
import urllib.request
import platform


# classes:
class SuperButton(Button):
    def change_text_color(self, new_colour):
        self.textColour = new_colour
        self.text = self.font.render(self.string, True, self.textColour)

    def change_text(self, new_text):
        self.string = new_text
        self.text = self.font.render(self.string, True, self.textColour)


# берем картинки из бд)
to_be_or_not_to_be = 0
picture = []
external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')


def read_picture_from_sql():
    global to_be_or_not_to_be
    global picture
    db = 'painterly_base.db'
    table = 'settings'
    id = ['1', '2', '3', '4', '5', '6', '7', '8']
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        to_be_or_not_to_be = 1
        for el in id:
            que = 'SELECT image, path FROM ' + table + ' WHERE id= "'+el+'"'
            cur.execute(que)
            rec = cur.fetchone()
            p_b = rec[0]
            p_p_init = rec[1]
            f_path, f_name = os.path.split(p_p_init)
            # путь к директории с кодом, пример моей директории
            n_path = f_name
            write_p_from_binary(n_path, p_b)
            picture.append(f_name)
    except:
        pass


def write_p_from_binary(f_path, p_b):
    f = open(f_path, 'wb')
    f.write(p_b)


read_picture_from_sql()


# drawing:
def drawing():
    if not toolbar.collidepoint((x, y)) and not toolbar2.collidepoint((x, y)):
        if pipet_mode:
            this_color = window.get_at((x, y))[:3]
            slider_r.value, slider_g.value, slider_b.value = this_color
            player_color_info()
        elif not o_m:
            if shape == 'circle':
                pg.draw.circle(latest1, clr, (x, y), r)
            # остроугольные треугольники
            elif shape == 'right_triangle':
                pg.draw.polygon(latest1, clr, [(x, y - side_1,), (x, y + side_1), (x + side_1, y)])
            elif shape == 'triangle':
                pg.draw.polygon(latest1, clr, [(x, y - side_1,), (x + side_1, y + side_1), (x - side_1, y + side_1)])
            elif shape == 'left_triangle':
                pg.draw.polygon(latest1, clr, [(x, y - side_1), (x, y + side_1), (x - side_1, y)])
            elif shape == 'down_triangle':
                pg.draw.polygon(latest1, clr, [(x, y + side_1,), (x + side_1, y - side_1), (x - side_1, y - side_1)])
            # прямоугольники и квадрат
            elif shape == 'rectangle':
                pg.draw.rect(latest1, clr, (x - side_1 // 2, y - side_2 // 2, side_1, side_2))
            elif shape == 'rectangle_1_2':
                pg.draw.rect(latest1, clr, (x - side_1 // 2, y - side_2 // 2, side_1, 2 * side_2))
            elif shape == 'rectangle_1_3':
                pg.draw.rect(latest1, clr, (x - side_1 // 2, y - side_2 // 2, side_1, 3 * side_2))
            elif shape == 'rectangle_2_1':
                pg.draw.rect(latest1, clr, (x - side_1 // 2, y - side_2 // 2, 2 * side_1, side_2))
            elif shape == 'rectangle_3_1':
                pg.draw.rect(latest1, clr, (x - side_1 // 2, y - side_2 // 2, 3 * side_1, side_2))
            # прямые треугольники
            elif shape == 'triangle_90':
                pg.draw.polygon(latest1, clr, [(x, y - side_1,), (x + side_1, y + side_1), (x, y + side_1)])
            elif shape == 'triangle_90_otr':
                pg.draw.polygon(latest1, clr, [(x, y - side_1,), (x - side_1, y + side_1), (x, y + side_1)])
            elif shape == 'left_triangle_90':
                pg.draw.polygon(latest1, clr, [(x, y), (x, y + side_1), (x - 2 * side_1, y + side_1)])
            elif shape == 'left_triangle_90_otr':
                pg.draw.polygon(latest1, clr, [(x, y + 2 * side_1), (x, y + side_1), (x - 2 * side_1, y + side_1)])
            elif shape == 'down_triangle_90':
                pg.draw.polygon(latest1, clr, [(x, y), (x + side_1, y), (x, y + 2 * side_1)])
            elif shape == 'down_triangle_90_otr':
                pg.draw.polygon(latest1, clr, [(x, y), (x - side_1, y), (x, y + 2 * side_1)])
            elif shape == 'right_triangle_90':
                pg.draw.polygon(latest1, clr, [(x, y), (x, y + side_1), (x + 2 * side_1, y + side_1)])
            elif shape == 'right_triangle_90_otr':
                pg.draw.polygon(latest1, clr, [(x, y + side_1), (x, y), (x + 2 * side_1, y)])
            # тупоугольные треугольники
            elif shape == 'triangle_more90':
                pg.draw.polygon(latest1, clr, [(x, y), (x + 2 * side_1, y), (x - 0.5 * side_1, y - side_1)])
            elif shape == 'triangle_more90_otr':
                pg.draw.polygon(latest1, clr, [(x, y), (x + 2 * side_1, y), (x + 2.5 * side_1, y - side_1)])
            elif shape == 'left_triangle_more90':
                pg.draw.polygon(latest1, clr, [(x, y), (x + 0.5 * side_1, y - 2 * side_1), (x - side_1, y)])
            elif shape == 'left_triangle_more90_otr':
                pg.draw.polygon(latest1, clr, [(x, y), (x + 0.5 * side_1, y + 2 * side_1), (x - side_1, y)])
            elif shape == 'down_triangle_more90':
                pg.draw.polygon(latest1, clr, [(x, y), (x - 2 * side_1, y), (x + 0.5 * side_1, y + side_1)])
            elif shape == 'down_triangle_more90_otr':
                pg.draw.polygon(latest1, clr, [(x, y), (x - 2 * side_1, y), (x - 2.5 * side_1, y + side_1)])
            elif shape == 'right_triangle_more90':
                pg.draw.polygon(latest1, clr, [(x, y), (x - 0.5 * side_1, y - 2 * side_1), (x + side_1, y)])
            elif shape == 'right_triangle_more90_otr':
                pg.draw.polygon(latest1, clr, [(x, y), (x - 0.5 * side_1, y + 2 * side_1), (x + side_1, y)])
        else:
            if shape == 'circle':
                pg.gfxdraw.circle(latest1, x, y, r, clr)
            # остроугольные треугольники
            elif shape == 'right_triangle':
                pg.gfxdraw.polygon(latest1, [(x, y - side_1,), (x, y + side_1), (x + side_1, y)], clr)
            elif shape == 'triangle':
                pg.gfxdraw.polygon(latest1, [(x, y - side_1,), (x + side_1, y + side_1), (x - side_1, y + side_1)], clr)
            elif shape == 'left_triangle':
                pg.gfxdraw.polygon(latest1, [(x, y - side_1), (x, y + side_1), (x - side_1, y)], clr)
            elif shape == 'down_triangle':
                pg.gfxdraw.polygon(latest1, [(x, y + side_1,), (x + side_1, y - side_1), (x - side_1, y - side_1)], clr)
            # прямоугольники и квадрат
            elif shape == 'rectangle':
                pg.gfxdraw.rectangle(latest1, (x - side_1 // 2, y - side_2 // 2, side_1, side_2), clr)
            elif shape == 'rectangle_1_2':
                pg.gfxdraw.rectangle(latest1, (x - side_1 // 2, y - side_2 // 2, side_1, 2 * side_2), clr)
            elif shape == 'rectangle_1_3':
                pg.gfxdraw.rectangle(latest1, (x - side_1 // 2, y - side_2 // 2, side_1, 3 * side_2), clr)
            elif shape == 'rectangle_2_1':
                pg.gfxdraw.rectangle(latest1, (x - side_1 // 2, y - side_2 // 2, 2 * side_1, side_2), clr)
            elif shape == 'rectangle_3_1':
                pg.gfxdraw.rectangle(latest1, (x - side_1 // 2, y - side_2 // 2, 3 * side_1, side_2), clr)
            # прямые треугольники
            elif shape == 'triangle_90':
                pg.gfxdraw.polygon(latest1, [(x, y - side_1,), (x + side_1, y + side_1), (x, y + side_1)], clr)
            elif shape == 'triangle_90_otr':
                pg.gfxdraw.polygon(latest1, [(x, y - side_1,), (x - side_1, y + side_1), (x, y + side_1)], clr)
            elif shape == 'left_triangle_90':
                pg.gfxdraw.polygon(latest1, [(x, y), (x, y + side_1), (x - 2 * side_1, y + side_1)], clr)
            elif shape == 'left_triangle_90_otr':
                pg.gfxdraw.polygon(latest1, [(x, y + 2 * side_1), (x, y + side_1), (x - 2 * side_1, y + side_1)], clr)
            elif shape == 'down_triangle_90':
                pg.gfxdraw.polygon(latest1, [(x, y), (x + side_1, y), (x, y + 2 * side_1)], clr)
            elif shape == 'down_triangle_90_otr':
                pg.gfxdraw.polygon(latest1, [(x, y), (x - side_1, y), (x, y + 2 * side_1)], clr)
            elif shape == 'right_triangle_90':
                pg.gfxdraw.polygon(latest1, [(x, y), (x, y + side_1), (x + 2 * side_1, y + side_1)], clr)
            elif shape == 'right_triangle_90_otr':
                pg.gfxdraw.polygon(latest1, [(x, y + side_1), (x, y), (x + 2 * side_1, y)], clr)
            # тупоугольные треугольники
            elif shape == 'triangle_more90':
                pg.gfxdraw.polygon(latest1, [(x, y), (x + 2 * side_1, y), (x - 0.5 * side_1, y - side_1)], clr)
            elif shape == 'triangle_more90_otr':
                pg.gfxdraw.polygon(latest1, [(x, y), (x + 2 * side_1, y), (x + 2.5 * side_1, y - side_1)], clr)
            elif shape == 'left_triangle_more90':
                pg.gfxdraw.polygon(latest1, [(x, y), (x + 0.5 * side_1, y - 2 * side_1), (x - side_1, y)], clr)
            elif shape == 'left_triangle_more90_otr':
                pg.gfxdraw.polygon(latest1, [(x, y), (x + 0.5 * side_1, y + 2 * side_1), (x - side_1, y)], clr)
            elif shape == 'down_triangle_more90':
                pg.gfxdraw.polygon(latest1, [(x, y), (x - 2 * side_1, y), (x + 0.5 * side_1, y + side_1)], clr)
            elif shape == 'down_triangle_more90_otr':
                pg.gfxdraw.polygon(latest1, [(x, y), (x - 2 * side_1, y), (x - 2.5 * side_1, y + side_1)], clr)
            elif shape == 'right_triangle_more90':
                pg.gfxdraw.polygon(latest1, [(x, y), (x - 0.5 * side_1, y - 2 * side_1), (x + side_1, y)], clr)
            elif shape == 'right_triangle_more90_otr':
                pg.gfxdraw.polygon(latest1, [(x, y), (x - 0.5 * side_1, y + 2 * side_1), (x + side_1, y)], clr)


def drawing_overlay():
    if not pipet_mode:
        if shape == 'circle':
            if r > 1:
                pg.gfxdraw.circle(overlay, x, y, r, clr)
        elif shape == 'rectangle':
            pygame.gfxdraw.rectangle(overlay,
                                     (x - side_1 // 2, y - side_2 // 2, side_1, side_2), clr)
        elif shape == 'right_triangle':
            pygame.gfxdraw.polygon(overlay,
                                   [(x, y - side_1,), (x, y + side_1),
                                    (x + side_1, y)], clr)
        elif shape == 'triangle':
            pygame.gfxdraw.polygon(overlay,
                                   [(x, y - side_1),
                                    (x + side_1, y + side_1),
                                    (x - side_1, y + side_1)], clr)
        elif shape == 'left_triangle':
            pygame.gfxdraw.polygon(overlay, [(x, y - side_1),
                                             (x, y + side_1),
                                             (x - side_1, y)], clr)
        elif shape == 'down_triangle':
            pygame.gfxdraw.polygon(overlay, [(x, y + side_1),
                                             (x + side_1, y - side_1),
                                             (x - side_1, y - side_1)], clr)
        # rectangle
        elif shape == 'rectangle_1_2':
            pygame.gfxdraw.rectangle(overlay, (x - side_1 // 2, (y - side_2 // 2), side_1, 2 * side_2), clr)
        elif shape == 'rectangle_1_3':
            pygame.gfxdraw.rectangle(overlay, (x - side_1 // 2, (y - side_2 // 2), side_1, 3 * side_2), clr)
        elif shape == 'rectangle_2_1':
            pygame.gfxdraw.rectangle(overlay, (x - side_1 // 2, (y - side_2 // 2), 2 * side_1, side_2), clr)
        elif shape == 'rectangle_3_1':
            pygame.gfxdraw.rectangle(overlay, (x - side_1 // 2, (y - side_2 // 2), 3 * side_1, side_2), clr)
        # triangle_90
        elif shape == 'triangle_90':
            pygame.gfxdraw.polygon(overlay, [(x, y - side_1,), (x + side_1, y + side_1), (x, y + side_1)], clr)
        elif shape == 'triangle_90_otr':
            pygame.gfxdraw.polygon(overlay, [(x, y - side_1,), (x - side_1, y + side_1), (x, y + side_1)], clr)
        elif shape == 'left_triangle_90':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x, y + side_1), (x - 2 * side_1, y + side_1)], clr)
        elif shape == 'left_triangle_90_otr':
            pygame.gfxdraw.polygon(overlay, [(x, y + 2 * side_1), (x, y + side_1), (x - 2 * side_1, y + side_1)], clr)
        elif shape == 'down_triangle_90':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x + side_1, y), (x, y + 2 * side_1)], clr)
        elif shape == 'down_triangle_90_otr':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x - side_1, y), (x, y + 2 * side_1)], clr)
        elif shape == 'right_triangle_90':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x, y + side_1), (x + 2 * side_1, y + side_1)], clr)
        elif shape == 'right_triangle_90_otr':
            pygame.gfxdraw.polygon(overlay, [(x, y + side_1), (x, y), (x + 2 * side_1, y)], clr)
        # triangle_more90
        elif shape == 'triangle_more90':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x + 2 * side_1, y), (x - 0.5 * side_1, y - side_1)], clr)
        elif shape == 'triangle_more90_otr':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x + 2 * side_1, y), (x + 2.5 * side_1, y - side_1)], clr)
        elif shape == 'left_triangle_more90':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x + 0.5 * side_1, y - 2 * side_1), (x - side_1, y)], clr)
        elif shape == 'left_triangle_more90_otr':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x + 0.5 * side_1, y + 2 * side_1), (x - side_1, y)], clr)
        elif shape == 'down_triangle_more90':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x - 2 * side_1, y), (x + 0.5 * side_1, y + side_1)], clr)
        elif shape == 'down_triangle_more90_otr':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x - 2 * side_1, y), (x - 2.5 * side_1, y + side_1)], clr)
        elif shape == 'right_triangle_more90':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x - 0.5 * side_1, y - 2 * side_1), (x + side_1, y)], clr)
        elif shape == 'right_triangle_more90_otr':
            pygame.gfxdraw.polygon(overlay, [(x, y), (x - 0.5 * side_1, y + 2 * side_1), (x + side_1, y)], clr)


def painting():
    global ongoing, undone, maxundone
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
            if maxundone < 10:
                maxundone += 1
            ongoing = False
    if screen in dirtyrects:
        # Drawing canvas:
        window.fill(white)
        for layer_ in layers:
            if layers.index(layer_) == undone:
                window.blit(pg.transform.smoothscale(layer_, (screen[2], screen[3])), screen)
        # Drawing overlay:
        overlay.fill(clear)
        drawing_overlay()


# size_monitor:
def monitor_size():
    mon = str(*(get_monitors()))[24:41].split()
    width = int(mon[0][:-1])
    height = int(mon[1][7:])
    return width, height


# shift:
def shiftdown():
    for layer_ in reversed(layers):
        if layer_ == latest10:
            window.blit(latest10, (0, 0))
        else:
            layers[layers.index(layer_)+1].blit(layer_, (0, 0))


def shiftup():
    for layer_ in layers:
        if layer_ == latest10:
            layer_.fill(clear)
        else:
            layer_.fill(clear)
            layer_.blit(layers[layers.index(layer_)+1], (0, 0))


# change_shape:
def change_shape_circle():
    global shape, button_rectangle, button_triangle, button_circle
    all_shape_white()
    a_button.change_text_color(green)
    shape = 'circle'


def change_shape_rectangle():
    global shape, button_rectangle, button_triangle, button_circle
    all_shape_white()
    s_button.change_text_color(green)
    shape = 'rectangle'


def change_shape_triangle():
    global shape, button_rectangle, button_triangle, button_circle
    all_shape_white()
    d_button.change_text_color(green)
    shape = 'triangle'


def changing_brush_size():
    global r, side_1, side_2
    if shape == 'circle':
        if event.button == 4 and r < 100:
            r += 1
            dirtyrects.append(screen)
        elif event.button == 5 and r > 2:
            r -= 1
            dirtyrects.append(screen)
    elif shape == 'rectangle':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'right_triangle':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'triangle':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'left_triangle':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'down_triangle':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'rectangle_1_2':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'rectangle_1_3':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'rectangle_2_1':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'rectangle_3_1':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'triangle_90':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'triangle_90_otr':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'left_triangle_90':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'left_triangle_90_otr':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'down_triangle_90':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'down_triangle_90_otr':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'right_triangle_90':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'right_triangle_90_otr':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'triangle_more90':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'triangle_more90_otr':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'left_triangle_more90':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'left_triangle_more90_otr':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'down_triangle_more90':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'down_triangle_more90_otr':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'right_triangle_more90':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)
    elif shape == 'right_triangle_more90_otr':
        if event.button == 4 and side_1 < 160 and side_2 < 160:
            side_1 += 1
            side_2 += 1
            dirtyrects.append(screen)
        elif event.button == 5 and side_1 > 2 and side_2 > 2:
            side_1 -= 1
            side_2 -= 1
            dirtyrects.append(screen)


def interaction_with_shapes():
    global shape, triangle_now, triangle_now_90, triangle_now_more90, all_triangle_now, rectangle_now
    if shape in types_of_triangle and event.key == pygame.K_LEFT:
        triangle_now += 1
        if triangle_now > 3:
            triangle_now = 0
        shape = types_of_triangle[triangle_now]
    elif shape in types_of_triangle and event.key == pygame.K_RIGHT:
        triangle_now -= 1
        if triangle_now < 0:
            triangle_now = 3
        shape = types_of_triangle[triangle_now]
    elif shape in types_of_rectangle and event.key == pygame.K_RIGHT:
        rectangle_now -= 1
        if rectangle_now < 0:
            rectangle_now = 4
        shape = types_of_rectangle[rectangle_now]
    elif shape in types_of_rectangle and event.key == pygame.K_LEFT:
        rectangle_now += 1
        if rectangle_now > 4:
            rectangle_now = 0
        shape = types_of_rectangle[rectangle_now]
    ######################################################################
    # triangle change type
    elif (shape in types_of_triangle or shape in types_of_triangle_90 or shape in types_of_triangle_more90) \
            and event.key == pygame.K_UP:
        all_triangle_now += 1
        if all_triangle_now > 2:
            all_triangle_now = 0
        shape = all_triangle[all_triangle_now]

    elif (shape in types_of_triangle or shape in types_of_triangle_90 or shape in types_of_triangle_more90) \
            and event.key == pygame.K_DOWN:
        all_triangle_now -= 1
        if all_triangle_now < 0:
            all_triangle_now = 2
        shape = all_triangle[all_triangle_now]
    ######################################################################
    # triangle_90
    elif shape in types_of_triangle_90 and event.key == pygame.K_LEFT:
        triangle_now_90 += 1
        if triangle_now_90 > 7:
            triangle_now_90 = 0
        shape = types_of_triangle_90[triangle_now_90]
    elif shape in types_of_triangle_90 and event.key == pygame.K_RIGHT:
        triangle_now_90 -= 1
        if triangle_now_90 < 0:
            triangle_now_90 = 7
        shape = types_of_triangle_90[triangle_now_90]
    # triangle_more90
    elif shape in types_of_triangle_more90 and event.key == pygame.K_LEFT:
        triangle_now_more90 += 1
        if triangle_now_more90 > 7:
            triangle_now_more90 = 0
        shape = types_of_triangle_more90[triangle_now_more90]
    elif shape in types_of_triangle_more90 and event.key == pygame.K_RIGHT:
        triangle_now_more90 -= 1
        if triangle_now_more90 < 0:
            triangle_now_more90 = 7
        shape = types_of_triangle_more90[triangle_now_more90]


# colors:
def all_shape_white():
    a_button.change_text_color(white)
    s_button.change_text_color(white)
    d_button.change_text_color(white)


def all_numbers_white():
    button_1.change_text_color(white)
    button_2.change_text_color(white)
    button_3.change_text_color(white)
    button_4.change_text_color(white)
    button_5.change_text_color(white)
    button_6.change_text_color(white)
    button_7.change_text_color(white)
    button_8.change_text_color(white)
    button_9.change_text_color(white)
    button_0.change_text_color(white)


def black_color():
    global clr
    clr = black
    all_numbers_white()
    button_1.change_text_color(green)


def white_color():
    global clr
    clr = white
    all_numbers_white()
    button_2.change_text_color(green)


def red_color():
    global clr
    clr = red
    all_numbers_white()
    button_3.change_text_color(green)


def orange_color():
    global clr
    clr = orange
    all_numbers_white()
    button_4.change_text_color(green)


def yellow_color():
    global clr
    clr = yellow
    all_numbers_white()
    button_5.change_text_color(green)


def green_color():
    global clr
    clr = green
    all_numbers_white()
    button_6.change_text_color(green)


def blue_color():
    global clr
    clr = blue
    all_numbers_white()
    button_7.change_text_color(green)


def purple_color():
    global clr
    clr = purple
    all_numbers_white()
    button_8.change_text_color(green)


def brown_color():
    global clr
    clr = brown
    all_numbers_white()
    button_9.change_text_color(green)


def player_color():
    global clr
    clr = (slider_r.value, slider_g.value, slider_b.value)
    all_numbers_white()
    button_0.change_text_color(green)


def player_color_info():
    text_box_r.setText(slider_r.getValue())
    text_box_g.setText(slider_g.getValue())
    text_box_b.setText(slider_b.getValue())
    button_player_colour.inactiveColour = (slider_r.value, slider_g.value, slider_b.value)
    button_player_colour.hoverColour = (slider_r.value, slider_g.value, slider_b.value)


# buttons_func:
def save_image():
    db = 'painterly_base.db'
    global external_ip
    con = sqlite3.connect(db)
    cur = con.cursor()
    que = f'SELECT login FROM users WHERE ip="{external_ip}"'
    cur.execute(que)
    rec = cur.fetchall()
    l = (rec[0])[0]
    que = f'SELECT password FROM users WHERE ip="{external_ip}"'
    cur.execute(que)
    rec = cur.fetchall()
    p = (rec[0])[0]
    # качаем картинку
    nam = 'image_from_Painterly'
    pygame.image.save(window, f"{nam}.png")
    pict_path = f"{nam}.png"
    f = open(pict_path, 'rb')
    p_b = f.read()
    b_p = p_b
    # переводим ее в блоб для записи в бд
    table = f'{l}_{p}'
    # тут пишешь название картинки на устройстве
    q_c = f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB, name TEXT)"
    cur.execute(q_c)
    # в str() ты указываешь номер id, просто с каждой слейдующей картинку прибавляй 1
    image = (b_p, pict_path,)
    que = f"INSERT INTO '{table}'(image, name) VALUES(?, ?)"
    cur.execute(que, image)
    con.commit()
    que = f"SELECT id FROM '{table}'"
    cur.execute(que)
    rec = cur.fetchall()
    if len(rec) > 6:
        for i in range(len(rec) - 6):
            zn = rec[i][0]
            que = f"DELETE FROM '{table}' WHERE id='{zn}'"
            cur.execute(que)
            con.commit()
    cur.close()
    con.close()




def clear_func():
    global undone, maxundone
    window.fill(white)
    latest10.fill(clear)
    latest9.fill(clear)
    latest8.fill(clear)
    latest7.fill(clear)
    latest6.fill(clear)
    latest5.fill(clear)
    latest4.fill(clear)
    latest3.fill(clear)
    latest2.fill(clear)
    latest1.fill(clear)
    undone = 0
    maxundone = 0
    dirtyrects.append(screen)


def locked_cord_x():
    global locked_x, language_now, text_locked_x
    if not locked_x:
        locked_x = True
        color_locked_x = green
        if language_now == 'Eng':
            text_locked_x = 'locked "x" = True'
        elif language_now == 'Rus':
            text_locked_x = '"x" закреплён'
    else:
        locked_x = False
        color_locked_x = white
        if language_now == 'Eng':
            text_locked_x = 'locked "x" = False'
        elif language_now == 'Rus':
            text_locked_x = '"x"  не закреплён'
    button_locked_x.change_text_color(color_locked_x)
    button_locked_x.change_text(text_locked_x)


def locked_cord_y():
    global locked_y, language_now, text_locked_y
    if not locked_y:
        locked_y = True
        color_locked_y = green
        if language_now == 'Eng':
            text_locked_y = 'locked "y" = True'
        elif language_now == 'Rus':
            text_locked_y = '"y" закреплён'
    else:
        locked_y = False
        color_locked_y = white
        if language_now == 'Eng':
            text_locked_y = 'locked "y" = False'
        elif language_now == 'Rus':
            text_locked_y = '"y"  не закреплён'
    button_locked_y.change_text_color(color_locked_y)
    button_locked_y.change_text(text_locked_y)


def overlay_shape():
    global o_m
    if not o_m:
        o_m = True
        r_button.change_text_color(green)
    else:
        o_m = False
        r_button.change_text_color(white)


def pipet():
    global pipet_mode
    if not pipet_mode:
        pipet_mode = True
        f_button.change_text_color(green)
    else:
        pipet_mode = False
        f_button.change_text_color(white)


# start:
def play():
    menu.clear()
    db = 'painterly_base.db'
    try:
        global done_login, done_passw, external_ip
        con = sqlite3.connect(db)
        cur = con.cursor()
        que = 'SELECT ip FROM users'
        cur.execute(que)
        rec = cur.fetchall()
        cur.close()
        for el in rec:
            if external_ip == el[0]:
                menu.disable()
        if language_now == 'Eng':
            menu.add.text_input('Login: ', default=done_login, maxchar=16, onreturn=check_log_login)
            menu.add.text_input('Password: ', default=done_passw, maxchar=16, onreturn=check_log_password)
            menu.add.button('Done', real_play2)
            menu.add.button('Back', main_menu)

        elif language_now == 'Rus':
            menu.add.text_input('Логин: ', default=done_login, maxchar=16, onreturn=check_log_login)
            menu.add.text_input('Пароль: ', default=done_passw, maxchar=16, onreturn=check_log_password)
            menu.add.button('Готово', real_play2)
            menu.add.button('Назад', main_menu)
    except:
        if language_now == 'Eng':
            menu.add.label('The database required for the application to work was not found on the device')
            menu.add.button('Back', main_menu)
        elif language_now == 'Rus':
            menu.add.label('На устройстве не найдена база данных, необходимая для работы приложения')
            menu.add.button('Назад', main_menu)


def exit_game():
    if os.path.exists('circle.jpg'):
        os.remove('circle.jpg')
    if os.path.exists('треугольник.png'):
        os.remove('треугольник.png')
    if os.path.exists('прямоугольник.jpg'):
        os.remove('прямоугольник.jpg')
    if os.path.exists('рамка.jpg'):
        os.remove('рамка.jpg')
    if os.path.exists('menu.jpg'):
        os.remove('menu.jpg')
    if os.path.exists('c.png'):
        os.remove('c.png')
    if os.path.exists('f.png'):
        os.remove('f.png')
    if os.path.exists('сатана.png'):
        os.remove('сатана.png')
    if os.path.exists('image_from_Painterly.png'):
        os.remove('image_from_Painterly.png')
    if os.path.exists('image1.png'):
        os.remove('image1.png')
    if os.path.exists('image2.png'):
        os.remove('image2.png')
    if os.path.exists('image3.png'):
        os.remove('image3.png')
    if os.path.exists('image4.png'):
        os.remove('image4.png')
    if os.path.exists('image5.png'):
        os.remove('image5.png')
    if os.path.exists('image6.png'):
        os.remove('image6.png')
    pg.quit()
    sys.exit()


def main_menu():
    global menu_exist, menu, person, registration_done
    if menu_exist:
        menu.clear()
    else:
        menu = pygame_menu.Menu('Painterly', monitor[0], monitor[1], theme=my_theme)
        menu_exist = True
    if language_now == 'Eng':
        menu.add.button('Enter', play, font_size=70)
        menu.add.button('Log out of your account', bb, font_size=70)
        menu.add.button('Profile', profile, font_size=70)
        menu.add.button('Settings', settings, font_size=70)
        menu.add.button('About the game', about, font_size=70)
        menu.add.button('Quit', exit_game, font_size=70)
    elif language_now == 'Rus':
        menu.add.button('Войти', play, font_size=70)
        menu.add.button('Выйти из аккаунта', bb, font_size=70)
        menu.add.button('Профиль', profile, font_size=70)
        menu.add.button('Настройки', settings, font_size=70)
        menu.add.button('Об игре', about, font_size=70)
        menu.add.button('Выход', exit_game, font_size=70)


def about():
    menu.clear()
    special_color = (255, 112, 41)
    if language_now == 'Eng':
        menu.add.label('Creators', font_color=special_color, font_shadow=False, font_size=75)
        menu.add.label('Nikita Murashov and Nadezhda Smirnova', font_size=30)
        menu.add.label('Team - "Painterly"', font_size=30)
        menu.add.button('VK community - link', vk, font_size=30)
        menu.add.label('Control', font_color=special_color, font_shadow=False, font_size=75)
        menu.add.label('Scrolling the mouse wheel changes the size of the shape.', font_size=30)
        menu.add.label('Buttons: "A", "S", "D" change the shape type.', font_size=30)
        menu.add.label('The numbers on the keyboard change the color of the shape.', font_size=30)
        menu.add.label('"Q" rolls back the action, "E" returns.', font_size=30)
        menu.add.label('"F", "R", "C" change the drawing mode.', font_size=30)
        menu.add.label('"X", "Y" limit the drawing coordinates.', font_size=30)
        menu.add.label('Сonventions', font_color=special_color, font_shadow=False, font_size=85)
        menu.add.label('The login must have letters.', font_size=30)
        menu.add.label('The login and password must not contain characters other than letters and numbers.', font_size=30)
        menu.add.label('After filling in the line, press "Enter".', font_size=30)
        menu.add.button('Back', main_menu, font_size=50)
    elif language_now == 'Rus':
        menu.add.label('Создатели', font_color=special_color, font_shadow=False, font_size=85)
        menu.add.label('Мурашов Никита и Надежда Смирнова', font_size=30)
        menu.add.label('Команда - "Painterly"', font_size=30)
        menu.add.button('Сообщество в вк - ссылка', vk, font_size=30)
        menu.add.label('Управление', font_color=special_color, font_shadow=False, font_size=85)
        menu.add.label('Прокрутка колесика мыши изменяет размер фигуры', font_size=30)
        menu.add.label('Кнопки: "A", "S", "D" изменяют тип фигуры.', font_size=30)
        menu.add.label('Цифры на клавиатуре изменяют цвет фигуры.', font_size=30)
        menu.add.label('"Q" откатывает действие, "E" - возвращает.', font_size=30)
        menu.add.label('"F", "R", "C" изменяют режим рисования.', font_size=30)
        menu.add.label('"X", "Y" ограничивают координаты рисования.', font_size=30)
        menu.add.label('Условности', font_color=special_color, font_shadow=False, font_size=85)
        menu.add.label('В логине обязательно должны быть буквы.', font_size=30)
        menu.add.label('В логине и пароле не должны быть символы кроме букв и цифр.', font_size=30)
        menu.add.label('После заполнения строки необходимо нажимать "Enter".', font_size=30)
        menu.add.button('Назад', main_menu, font_size=50)


def vk():
    if platform.system() == 'Windows':
        os.system("start \"\" https://vk.com/Painterly_ru")
    elif platform.system() == 'Linux':
        os.system("xdg-open \"\" https://vk.com/Painterly_ru")
    else:
        os.system("open \"\" https://vk.com/Painterly_ru")


def bb():
    global registration_done, external_ip
    db = 'painterly_base.db'
    con = sqlite3.connect(db)
    cur = con.cursor()
    registration_done = False
    qry = f"UPDATE users SET ip='2' WHERE ip='{external_ip}'"
    cur.execute(qry)
    con.commit()


def real_game():
    menu.disable()


# для тех у кого уже есть аккаунт
def real_play2():
    db = 'painterly_base.db'
    con = sqlite3.connect(db)
    cur = con.cursor()
    global done_login, done_passw, password_res, login_res, registration_done, external_ip, y, x
    # если пользователь уже есть в бд
    if done_login != 'afhvgnf' and done_passw != 'nhmhhy78':
        registration_done = True
        qry = f"UPDATE users SET ip='{external_ip}' WHERE login='{done_login}'"
        cur.execute(qry)
        con.commit()
        menu.disable()
    # новый пользователь в бд
    else:
        if password_res != 'panda23ki' and login_res != 'hahahe7' and password_res.isalnum() and login_res.isalnum()\
                and login_res != 'afhvgnf' and password_res != 'nhmhhy78' and not login_res.isdigit():
            registration_done = True
            user = (password_res, login_res, external_ip)
            cur.execute("INSERT INTO users VALUES(?, ?, ?);", user)
            con.commit()
            menu.disable()
        else:
            menu.clear()
            if language_now == 'Eng':
                menu.add.label('Something went wrong. Check that the password and login are correct')
                menu.add.button('Back', play)
            if language_now == 'Rus':
                menu.add.label('Что-то пошло не так. Проверьте правильность пароля и логина.')
                menu.add.button('Назад', play)


def check_log_login(value):
    global done_login, login_res
    db = 'painterly_base.db'
    con = sqlite3.connect(db)
    cur = con.cursor()
    que = 'SELECT login FROM users'
    c = 0
    cur.execute(que)
    rec = cur.fetchall()
    for el in rec:
        if value != el[0]:
            c += 1
    if c != len(rec):
        done_login = value
    else:
        login_res = value


def check_log_password(value):
    global done_passw, password_res
    db = 'painterly_base.db'
    con = sqlite3.connect(db)
    cur = con.cursor()
    c = 0
    que = 'SELECT password FROM users'
    cur.execute(que)
    rec = cur.fetchall()
    for el in rec:
        if value != el[0]:
            c += 1
    if c == len(rec):
        password_res = value
    else:
        done_passw = value


def profile():
    global external_ip
    db = 'painterly_base.db'
    con = sqlite3.connect(db)
    cur = con.cursor()
    c = 0
    que = 'SELECT ip FROM users'
    cur.execute(que)
    rec = cur.fetchall()
    for el in rec:
        if external_ip == el[0]:
            c += 1
    if c > 0:
        que = f"SELECT login FROM users WHERE ip='{external_ip}'"
        cur.execute(que)
        rec = cur.fetchone()
        login_now = rec[0]
        que = f"SELECT password FROM users WHERE ip='{external_ip}'"
        cur.execute(que)
        rec = cur.fetchone()
        password_now = rec[0]
        menu.clear()
        greeting = menu.add.label(f'{login_now}',
                                  font_color=yandex_color,
                                  font_shadow=True,
                                  font_shadow_color=gray,
                                  font_size=100
                                  )
        greeting.translate(0, 100)
        # запрос на картинки в бд
        try:
            que = f"SELECT image from {login_now}_{password_now}"
            cur.execute(que)
            rec = cur.fetchall()
            n = 1
            for el in rec:
                f = open(f'image{n}.png', 'wb')
                f.write(el[0])
                n += 1
            if len(rec) == 1:
                image_1 = menu.add.image('рамка.jpg')
                image_1.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_1.translate(-monitor[0] // 3.49, monitor[1] // 5.1923076)
                image_2 = menu.add.image('рамка.jpg')
                image_2.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3 = menu.add.image('рамка.jpg')
                image_3.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3.translate(monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_4 = menu.add.image('рамка.jpg')
                image_4.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5 = menu.add.image('рамка.jpg')
                image_5.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5.translate(-monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_6 = menu.add.image('рамка.jpg')
                image_6.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_6.translate(monitor[0] // 3.49, -monitor[1] // 2.59615384)
            if len(rec) == 2:
                image_1 = menu.add.image('image1.png')
                image_1.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_1.translate(-monitor[0] // 3.49, monitor[1] // 5.1923076)
                image_2 = menu.add.image('рамка.jpg')
                image_2.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3 = menu.add.image('рамка.jpg')
                image_3.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3.translate(monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_4 = menu.add.image('рамка.jpg')
                image_4.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5 = menu.add.image('рамка.jpg')
                image_5.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5.translate(-monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_6 = menu.add.image('рамка.jpg')
                image_6.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_6.translate(monitor[0] // 3.49, -monitor[1] // 2.59615384)
            if len(rec) == 3:
                image_1 = menu.add.image('image1.png')
                image_1.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_1.translate(-monitor[0] // 3.49, monitor[1] // 5.1923076)
                image_2 = menu.add.image('image2.png')
                image_2.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3 = menu.add.image('рамка.jpg')
                image_3.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3.translate(monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_4 = menu.add.image('рамка.jpg')
                image_4.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5 = menu.add.image('рамка.jpg')
                image_5.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5.translate(-monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_6 = menu.add.image('рамка.jpg')
                image_6.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_6.translate(monitor[0] // 3.49, -monitor[1] // 2.59615384)
            if len(rec) == 4:
                image_1 = menu.add.image('image1.png')
                image_1.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_1.translate(-monitor[0] // 3.49, monitor[1] // 5.1923076)
                image_2 = menu.add.image('image2.png')
                image_2.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3 = menu.add.image('image3.png')
                image_3.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3.translate(monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_4 = menu.add.image('рамка.jpg')
                image_4.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5 = menu.add.image('рамка.jpg')
                image_5.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5.translate(-monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_6 = menu.add.image('рамка.jpg')
                image_6.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_6.translate(monitor[0] // 3.49, -monitor[1] // 2.59615384)
            if len(rec) == 5:
                image_1 = menu.add.image('image1.png')
                image_1.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_1.translate(-monitor[0] // 3.49, monitor[1] // 5.1923076)
                image_2 = menu.add.image('image2.png')
                image_2.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3 = menu.add.image('image3.png')
                image_3.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3.translate(monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_4 = menu.add.image('image4.png')
                image_4.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5 = menu.add.image('рамка.jpg')
                image_5.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5.translate(-monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_6 = menu.add.image('рамка.jpg')
                image_6.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_6.translate(monitor[0] // 3.49, -monitor[1] // 2.59615384)
            if len(rec) == 6:
                image_1 = menu.add.image('image1.png')
                image_1.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_1.translate(-monitor[0] // 3.49, monitor[1] // 5.1923076)
                image_2 = menu.add.image('image2.png')
                image_2.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3 = menu.add.image('image3.png')
                image_3.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_3.translate(monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_4 = menu.add.image('image4.png')
                image_4.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5 = menu.add.image('image5.png')
                image_5.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_5.translate(-monitor[0] // 3.49, -monitor[1] // 5.1923076)
                image_6 = menu.add.image('рамка.jpg')
                image_6.resize(monitor[0] // 6.4, monitor[1] // 5.4)
                image_6.translate(monitor[0] // 3.49, -monitor[1] // 2.59615384)
            if language_now == 'Eng':
                open_ = menu.add.button('Open', font_size=60)
                save_ = menu.add.button('Save', font_size=60)
                delete_ = menu.add.button('Delete', font_size=60)
                back = menu.add.button('Back', main_menu, font_size=60)
            elif language_now == 'Rus':
                open_ = menu.add.button('Открыть', font_size=60)
                save_ = menu.add.button('Сохранить', font_size=60)
                delete_ = menu.add.button('Удалить', font_size=60)
                back = menu.add.button('Назад', main_menu, font_size=60)
            open_.translate(0, -monitor[1] // 2.7)
            save_.translate(0, -monitor[1] // 2.7)
            delete_.translate(0, -monitor[1] // 2.7)
            back.translate(0, -monitor[1] // 2.7)
        except:
            menu.clear()
            if language_now == 'Eng':
                menu.add.label('You do not have any saved works yet')
                back = menu.add.button('Back', main_menu, font_size=60)
            elif language_now == 'Rus':
                menu.add.label('У вас еще нет сохраненных работ')
                back = menu.add.button('Назад', main_menu, font_size=60)

    else:
        menu.clear()
        if language_now == 'Eng':
            menu.add.label('Please log in to your account')
            menu.add.button('Back', main_menu)
        if language_now == 'Rus':
            menu.add.label('Войдите пожалуйста в аккаунт')
            menu.add.button('Назад', main_menu)

# для новых пользователей
def real_play():
    menu.disable()


def translate(_, value):
    global language_now, text_locked_x, text_locked_y, text_save
    if value == 'Russian':
        language_now = 'Rus'
        if button_locked_x.textColour == green:
            text_locked_x = '"x" закреплён'
        else:
            text_locked_x = '"x" не закреплён'
        if button_locked_y.textColour == green:
            text_locked_y = '"y" закреплён'
        else:
            text_locked_y = '"y" не закреплён'
        text_save = 'Сохранить'
    elif value == 'English':
        language_now = 'Eng'
        if button_locked_x.textColour == green:
            text_locked_x = 'locked "x" = True'
        else:
            text_locked_x = 'locked "x" = False'
        if button_locked_y.textColour == green:
            text_locked_y = 'locked "y" = True'
        else:
            text_locked_y = 'locked "y" = False'
        text_save = 'Save'
    button_locked_x.change_text(text_locked_x)
    button_locked_y.change_text(text_locked_x)
    save_button.change_text(text_save)
    settings()


def music(_, value):
    global music_now
    music_now = value
    pygame.mixer.music.pause()
    if value == 2:
        pygame.mixer.music.load('beach.mp3')
        pygame.mixer.music.play(-1)
    elif value == 3:
        pygame.mixer.music.load('inspiration.mp3')
        pygame.mixer.music.play(-1)
    elif value == 4:
        pygame.mixer.music.load('pixel.mp3')
        pygame.mixer.music.play(-1)


def settings():
    global music_now
    menu.clear()
    if language_now == 'Eng':
        menu.add.selector('Language: ', [('English', 'English'), ('Русский', 'Russian')], onchange=translate)
        music_button = menu.add.selector('Music: ', [('Silence', 1), ('Positive', 2), ('Inspiration', 3), ('Pixel', 4)],
                                         onchange=music)
        menu.add.button('Back', main_menu)
    elif language_now == 'Rus':
        menu.add.selector('Язык: ', [('Русский', 'Russian'), ('English', 'English')], onchange=translate)
        music_button = menu.add.selector('Музыка: ', [('Тишина', 1), ('Позитив', 2), ('Вдохновение', 3),
                                                      ('Пиксель', 4)],
                                         onchange=music)
        menu.add.button('Назад', main_menu)
    music_button.set_value(music_now - 1)


# update:
def updating():
    pygame_widgets.update(event)
    pg.display.update()
    pg.display.update(dirtyrects)


########################################################################################################################
pg.init()
# Settings:
monitor = monitor_size()
width_window = monitor[0]
length_window = monitor[1]
dirtyrects = list()
arrows = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
mousepos = (0, 0)
language_now = 'Rus'
music_now = 1
##############
done_login = 'afhvgnf'
done_passw = 'nhmhhy78'
surname_res = 'surname'
login_res = 'hahahe7'
password_res = 'panda23ki'
###############
x = 0
y = 0
# Colors | R | G | B | A |
clear = (0, 0, 0, 0)
white = (255, 255, 255)
gray = (209, 147, 92)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 125, 0)
yellow = (255, 255, 0)
green = (0, 225, 0)
blue = (0, 0, 255)
purple = (150, 0, 150)
brown = (117, 51, 19)
# wood = (179, 83, 0)
figure = [1, 2, 3]
yandex_color = (255, 204, 0)
#############
# menu:
my_theme = pygame_menu.themes.THEME_GREEN.copy()
my_theme.widget_font = 'VinnytsiaSerif.ttf'
my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
my_theme.title_font = pygame_menu.font.FONT_DIGITAL
my_theme.title_font_size = 75
my_image = pygame_menu.baseimage.BaseImage('menu.jpg')
my_theme.background_color = my_image
my_theme.title_background_color = clear
my_theme.title_font_color = yandex_color
my_theme.title_font_shadow = True
my_theme.title_offset = (40, 40)
my_theme.scrollbar_color = clear
my_theme.scrollbar_slider_color = clear
my_theme.scrollbar_slider_hover_color = clear
my_theme.scrollbar_thick = 6
my_theme.selection_color = clear
my_theme.widget_font_shadow = True
my_theme.widget_font_size = 50
my_theme.widget_font_color = (68, 187, 255)
# Surfaces:
window = pg.display.set_mode(monitor)
window.fill(white)
overlay = pg.Surface(monitor).convert_alpha()
# menu:
person = False
registration_done = False
menu_exist = False
main_menu()
# Rects:
screen = pg.Rect(0, 0, monitor[0], monitor[1])
toolbar = pg.Rect(0, length_window * 0.823, width_window, length_window * 0.178)
toolbar2 = pg.Rect(width_window * 0.9, 0, width_window * 0.11, length_window)
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
latest6 = overlay.copy()
latest7 = overlay.copy()
latest8 = overlay.copy()
latest9 = overlay.copy()
latest10 = overlay.copy()
layers = [latest1, latest2, latest3, latest4, latest5, latest6, latest7, latest8, latest9, latest10]
for layer in layers:
    layer.fill(clear)
pg.draw.rect(overlay, gray, toolbar)
pg.draw.rect(overlay, black, toolbar, 5)
pg.draw.rect(overlay, gray, toolbar2)
pg.draw.rect(overlay, black, toolbar2, 5)
overlaybg = overlay.copy()
# key_function:
locked_x = False
locked_y = False
# shapes:
clr = black
shape = 'circle'
r = 25
side_1 = 25
side_2 = 25
types_of_triangle = ['triangle', 'left_triangle', 'down_triangle', 'right_triangle']
types_of_triangle_90 = ['triangle_90', 'triangle_90_otr', 'left_triangle_90', 'left_triangle_90_otr',
                        'down_triangle_90_otr', 'down_triangle_90', 'right_triangle_90_otr', 'right_triangle_90']
types_of_triangle_more90 = ['triangle_more90', 'triangle_more90_otr', 'left_triangle_more90',
                            'left_triangle_more90_otr', 'down_triangle_more90', 'down_triangle_more90_otr',
                            'right_triangle_more90', 'right_triangle_more90_otr']
all_triangle = ['triangle', 'triangle_90', 'triangle_more90']
all_triangle_now = 0
triangle_now = 0
triangle_now_90 = 0
triangle_now_more90 = 0
types_of_rectangle = ['rectangle', 'rectangle_1_2', 'rectangle_2_1', 'rectangle_1_3', 'rectangle_3_1']
rectangle_now = 0
# Sliders:
slider_r = Slider(window,
                  int(width_window * 0.6),
                  int(length_window * 0.86),
                  int(width_window * 0.15),
                  int(length_window * 0.015),
                  min=0,
                  max=255,
                  step=1,
                  handleColour=red)
slider_r.value = 0
text_box_r = TextBox(window,
                     int(width_window * 0.76),
                     int(length_window * 0.845),
                     int(width_window * 0.03),
                     int(length_window * 0.045),
                     fontSize=30)
text_box_r.disable()
slider_g = Slider(window,
                  int(width_window * 0.6),
                  int(length_window * 0.91),
                  int(width_window * 0.15),
                  int(length_window * 0.015),
                  min=0,
                  max=255,
                  step=1,
                  handleColour=green)
slider_g.value = 0
text_box_g = TextBox(window,
                     int(width_window * 0.76),
                     int(length_window * 0.895),
                     int(width_window * 0.03),
                     int(length_window * 0.045),
                     fontSize=30)
text_box_g.disable()
slider_b = Slider(window,
                  int(width_window * 0.6),
                  int(length_window * 0.96),
                  int(width_window * 0.15),
                  int(length_window * 0.015),
                  min=0,
                  max=255,
                  step=1,
                  handleColour=blue)
slider_b.value = 0
text_box_b = TextBox(window,
                     int(width_window * 0.76),
                     int(length_window * 0.945),
                     int(width_window * 0.03),
                     int(length_window * 0.045),
                     fontSize=30)
text_box_b.disable()
# Buttons:
# если есть бд
if to_be_or_not_to_be == 1:
    if len(picture) >= 3:
        image = pygame.image.load(f'{picture[0]}')
        image = pygame.transform.scale(image, (int(monitor[0] * 0.057 - 10), int(monitor[1] * 0.1 - 10)))
        button_circle = SuperButton(window,
                                    int(monitor[0] * 0.935),
                                    int(monitor[1] * 0.05),
                                    int(monitor[0] * 0.057),
                                    int(monitor[1] * 0.1),
                                    inactiveColour=white,
                                    hoverColour=white,
                                    pressedColour=white,
                                    onClick=change_shape_circle,
                                    borderThickness=5,
                                    image=image)
        image = pygame.image.load(f'{picture[1]}')
        image = pygame.transform.scale(image, (int(monitor[0] * 0.057 - 10), int(monitor[1] * 0.1 - 10)))
        button_rectangle = SuperButton(window,
                                       int(monitor[0] * 0.935),
                                       int(monitor[1] * 0.18),
                                       int(monitor[0] * 0.057),
                                       int(monitor[1] * 0.1),
                                       inactiveColour=white,
                                       hoverColour=white,
                                       pressedColour=white,
                                       onClick=change_shape_rectangle,
                                       borderThickness=5,
                                       image=image)
        image = pygame.image.load(f'{picture[2]}')
        image = pygame.transform.scale(image, (int(monitor[0] * 0.057 - 10), int(monitor[1] * 0.1 - 10)))
        button_triangle = SuperButton(window,
                                      int(monitor[0] * 0.935),
                                      int(monitor[1] * 0.31),
                                      int(monitor[0] * 0.057),
                                      int(monitor[1] * 0.1),
                                      inactiveColour=white,
                                      hoverColour=white,
                                      pressedColour=white,
                                      onClick=change_shape_triangle,
                                      borderThickness=5,
                                      image=image)
        image = pygame.image.load(f'{picture[5]}')
        image = pygame.transform.scale(image, (int(monitor[0] * 0.057 - 10), int(monitor[1] * 0.1 - 10)))
        pipet_mode = False
        pipette = SuperButton(window,
                              int(monitor[0] * 0.935),
                              int(monitor[1] * 0.44),
                              int(monitor[0] * 0.057),
                              int(monitor[1] * 0.1),
                              inactiveColour=white,
                              hoverColour=white,
                              pressedColour=white,
                              onClick=pipet,
                              borderThickness=5,
                              image=image)

        image = pygame.image.load(f'{picture[6]}')
        image = pygame.transform.scale(image, (int(monitor[0] * 0.057 - 10), int(monitor[1] * 0.1 - 10)))
        clear_button = SuperButton(window,
                                   int(monitor[0] * 0.935),
                                   int(monitor[1] * 0.7),
                                   int(monitor[0] * 0.057),
                                   int(monitor[1] * 0.1),
                                   inactiveColour=white,
                                   hoverColour=white,
                                   pressedColour=white,
                                   onClick=clear_func,
                                   borderThickness=5,
                                   image=image)
        image = pygame.image.load(f'{picture[7]}')
        image = pygame.transform.scale(image, (int(monitor[0] * 0.057 - 10), int(monitor[1] * 0.1 - 10)))
        o_m = False
        overlay_mode = SuperButton(window,
                                   int(monitor[0] * 0.935),
                                   int(monitor[1] * 0.57),
                                   int(monitor[0] * 0.057),
                                   int(monitor[1] * 0.1),
                                   inactiveColour=white,
                                   hoverColour=white,
                                   pressedColour=white,
                                   onClick=overlay_shape,
                                   borderThickness=5,
                                   image=image)


# если нет бд
else:
    button_circle = SuperButton(window,
                                int(monitor[0] * 0.935),
                                int(monitor[1] * 0.05),
                                int(monitor[0] * 0.057),
                                int(monitor[1] * 0.1),
                                inactiveColour=white,
                                hoverColour=white,
                                pressedColour=white,
                                onClick=change_shape_circle,
                                borderThickness=5)
    button_rectangle = SuperButton(window,
                                   int(monitor[0] * 0.935),
                                   int(monitor[1] * 0.18),
                                   int(monitor[0] * 0.057),
                                   int(monitor[1] * 0.1),
                                   inactiveColour=white,
                                   hoverColour=white,
                                   pressedColour=white,
                                   onClick=change_shape_rectangle,
                                   borderThickness=5)
    button_triangle = SuperButton(window,
                                  int(monitor[0] * 0.935),
                                  int(monitor[1] * 0.31),
                                  int(monitor[0] * 0.057),
                                  int(monitor[1] * 0.1),
                                  inactiveColour=white,
                                  hoverColour=white,
                                  pressedColour=white,
                                  onClick=change_shape_triangle,
                                  borderThickness=5)
    pipet_mode = False
    pipette = SuperButton(window,
                          int(monitor[0] * 0.935),
                          int(monitor[1] * 0.44),
                          int(monitor[0] * 0.057),
                          int(monitor[1] * 0.1),
                          inactiveColour=white,
                          hoverColour=white,
                          pressedColour=white,
                          onClick=pipet,
                          borderThickness=5)

    clear_button = SuperButton(window,
                               int(monitor[0] * 0.935),
                               int(monitor[1] * 0.7),
                               int(monitor[0] * 0.057),
                               int(monitor[1] * 0.1),
                               inactiveColour=white,
                               hoverColour=white,
                               pressedColour=white,
                               onClick=clear_func,
                               borderThickness=5)

    o_m = False
    overlay_mode = SuperButton(window,
                               int(monitor[0] * 0.935),
                               int(monitor[1] * 0.57),
                               int(monitor[0] * 0.057),
                               int(monitor[1] * 0.1),
                               inactiveColour=white,
                               hoverColour=white,
                               pressedColour=white,
                               onClick=overlay_shape,
                               borderThickness=5)
a_button = SuperButton(window,
                       int(monitor[0] * 0.910),
                       int(monitor[1] * 0.072),
                       int(monitor[0] * 0.02),
                       int(monitor[1] * 0.05),
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray,
                       text='A',
                       fontSize=60,
                       textColour=white)
a_button.disable()
s_button = SuperButton(window,
                       int(monitor[0] * 0.910),
                       int(monitor[1] * 0.202),
                       int(monitor[0] * 0.02),
                       int(monitor[1] * 0.05),
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray,
                       text='S',
                       fontSize=60,
                       textColour=white)
s_button.disable()
d_button = SuperButton(window,
                       int(monitor[0] * 0.910),
                       int(monitor[1] * 0.332),
                       int(monitor[0] * 0.02),
                       int(monitor[1] * 0.05),
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray,
                       text='D',
                       fontSize=60,
                       textColour=white)
d_button.disable()
f_button = SuperButton(window,
                       int(monitor[0] * 0.910),
                       int(monitor[1] * 0.462),
                       int(monitor[0] * 0.02),
                       int(monitor[1] * 0.05),
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray,
                       text='F',
                       fontSize=60,
                       textColour=white)
f_button.disable()
r_button = SuperButton(window,
                       int(monitor[0] * 0.910),
                       int(monitor[1] * 0.592),
                       int(monitor[0] * 0.02),
                       int(monitor[1] * 0.05),
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray,
                       text='R',
                       fontSize=60,
                       textColour=white)
r_button.disable()
c_button = SuperButton(window,
                       int(monitor[0] * 0.910),
                       int(monitor[1] * 0.732),
                       int(monitor[0] * 0.02),
                       int(monitor[1] * 0.05),
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray,
                       text='C',
                       fontSize=60,
                       textColour=white)
c_button.disable()
if language_now == 'Eng':
    text_locked_x = 'locked "x" = False'
    text_locked_y = 'locked "y" = False'
    text_save = 'Save'
elif language_now == 'Rus':
    text_locked_x = '"x"  не закреплён'
    text_locked_y = '"y"  не закреплён'
    text_save = 'Сохранить'
button_locked_x = SuperButton(window,
                              int(monitor[0] * 0.925),
                              int(monitor[1] * 0.85),
                              int(monitor[0] * 0.057),
                              int(monitor[1] * 0.04),
                              text=text_locked_x,
                              textColour=white,
                              fontSize=30,
                              inactiveColour=gray,
                              hoverColour=gray,
                              pressedColour=gray)
button_locked_x.disable()
button_locked_y = SuperButton(window,
                              int(monitor[0] * 0.925),
                              int(monitor[1] * 0.9),
                              int(monitor[0] * 0.057),
                              int(monitor[1] * 0.04),
                              text=text_locked_y,
                              textColour=white,
                              fontSize=30,
                              inactiveColour=gray,
                              hoverColour=gray,
                              pressedColour=gray)
button_locked_y.disable()
save_button = SuperButton(window,
                          int(monitor[0] * 0.925),
                          int(monitor[1] * 0.95),
                          int(monitor[0] * 0.057),
                          int(monitor[1] * 0.025),
                          text=text_save,
                          textColour=white,
                          fontSize=25,
                          inactiveColour=purple,
                          hoverColour=purple,
                          pressedColour=green,
                          onClick=save_image,
                          borderThickness=2)
# colors:
button_0 = SuperButton(window,
                       int(monitor[0] * 0.88),
                       int(monitor[1] * 0.865),
                       int(monitor[0] * 0.001),
                       int(monitor[1] * 0.1),
                       text='0',
                       textColour=white,
                       fontSize=100,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_0.disable()
button_player_colour = SuperButton(window,
                                   int(monitor[0] * 0.8),
                                   int(monitor[1] * 0.865),
                                   int(monitor[0] * 0.057),
                                   int(monitor[1] * 0.1),
                                   inactiveColour=black,
                                   hoverColour=black,
                                   pressedColour=white,
                                   borderThickness=3,
                                   onClick=player_color,
                                   radius=100)
black_button = SuperButton(window,
                           int(monitor[0] * 0.025),
                           int(monitor[1] * 0.91),
                           int(monitor[0] * 0.05),
                           int(monitor[1] * 0.08),
                           inactiveColour=black,
                           hoverColour=black,
                           pressedColour=white,
                           borderThickness=3,
                           onClick=black_color,
                           radius=100)
button_1 = SuperButton(window,
                       int(monitor[0] * 0.025),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='1',
                       textColour=green,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_1.disable()
white_button = SuperButton(window,
                           int(monitor[0] * 0.087),
                           int(monitor[1] * 0.91),
                           int(monitor[0] * 0.05),
                           int(monitor[1] * 0.08),
                           inactiveColour=white,
                           hoverColour=white,
                           pressedColour=white,
                           borderThickness=3,
                           onClick=white_color,
                           radius=100)
button_2 = SuperButton(window,
                       int(monitor[0] * 0.087),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='2',
                       textColour=white,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_2.disable()
red_button = SuperButton(window,
                         int(monitor[0] * 0.149),
                         int(monitor[1] * 0.91),
                         int(monitor[0] * 0.05),
                         int(monitor[1] * 0.08),
                         inactiveColour=red,
                         hoverColour=red,
                         pressedColour=white,
                         borderThickness=3,
                         onClick=red_color,
                         radius=100)
button_3 = SuperButton(window,
                       int(monitor[0] * 0.149),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='3',
                       textColour=white,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_3.disable()
orange_button = SuperButton(window,
                            int(monitor[0] * 0.211),
                            int(monitor[1] * 0.91),
                            int(monitor[0] * 0.05),
                            int(monitor[1] * 0.08),
                            inactiveColour=orange,
                            hoverColour=orange,
                            pressedColour=white,
                            borderThickness=3,
                            onClick=orange_color,
                            radius=100)
button_4 = SuperButton(window,
                       int(monitor[0] * 0.211),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='4',
                       textColour=white,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_4.disable()
yellow_button = SuperButton(window,
                            int(monitor[0] * 0.273),
                            int(monitor[1] * 0.91),
                            int(monitor[0] * 0.05),
                            int(monitor[1] * 0.08),
                            inactiveColour=yellow,
                            hoverColour=yellow,
                            pressedColour=white,
                            borderThickness=3,
                            onClick=yellow_color,
                            radius=100)
button_5 = SuperButton(window,
                       int(monitor[0] * 0.273),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='5',
                       textColour=white,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_5.disable()
green_button = SuperButton(window,
                           int(monitor[0] * 0.335),
                           int(monitor[1] * 0.91),
                           int(monitor[0] * 0.05),
                           int(monitor[1] * 0.08),
                           inactiveColour=green,
                           hoverColour=green,
                           pressedColour=white,
                           borderThickness=3,
                           onClick=green_color,
                           radius=100)
button_6 = SuperButton(window,
                       int(monitor[0] * 0.335),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='6',
                       textColour=white,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_6.disable()
blue_button = SuperButton(window,
                          int(monitor[0] * 0.397),
                          int(monitor[1] * 0.91),
                          int(monitor[0] * 0.05),
                          int(monitor[1] * 0.08),
                          inactiveColour=blue,
                          hoverColour=blue,
                          pressedColour=white,
                          borderThickness=3,
                          onClick=blue_color,
                          radius=100)
button_7 = SuperButton(window,
                       int(monitor[0] * 0.397),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='7',
                       textColour=white,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_7.disable()
purple_button = SuperButton(window,
                            int(monitor[0] * 0.459),
                            int(monitor[1] * 0.91),
                            int(monitor[0] * 0.05),
                            int(monitor[1] * 0.08),
                            inactiveColour=purple,
                            hoverColour=purple,
                            pressedColour=white,
                            borderThickness=3,
                            onClick=purple_color,
                            radius=100)
button_8 = SuperButton(window,
                       int(monitor[0] * 0.459),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='8',
                       textColour=white,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_8.disable()
brown_button = SuperButton(window,
                           int(monitor[0] * 0.521),
                           int(monitor[1] * 0.91),
                           int(monitor[0] * 0.05),
                           int(monitor[1] * 0.08),
                           inactiveColour=brown,
                           hoverColour=brown,
                           pressedColour=white,
                           borderThickness=3,
                           onClick=brown_color,
                           radius=100)
button_9 = SuperButton(window,
                       int(monitor[0] * 0.521),
                       int(monitor[1] * 0.85),
                       int(monitor[0] * 0.05),
                       int(monitor[1] * 0.04),
                       text='9',
                       textColour=white,
                       fontSize=50,
                       inactiveColour=gray,
                       hoverColour=gray,
                       pressedColour=gray)
button_9.disable()
########################################################################################################################
menu.enable()
menu.mainloop(window)
while True:
    for event in pg.event.get():
        # exit:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # mouse_pos:
        if event.type == pg.MOUSEMOTION:
            mousepos = pg.mouse.get_pos()
            if not locked_x:
                x = mousepos[0]
            if not locked_y:
                y = mousepos[1]
            holdingclick = True
            if screen.collidepoint(mousepos):
                dirtyrects.append(screen)
            # mouse:
        if event.type == pg.MOUSEBUTTONDOWN:
            holdingclick = False
            if screen.collidepoint(mousepos):
                dirtyrects.append(screen)
            # Changing brush size:
            changing_brush_size()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                menu.enable()
                main_menu()
                menu.mainloop(window)
            elif event.key == pg.K_a:
                change_shape_circle()
            elif event.key == pg.K_s:
                change_shape_rectangle()
            elif event.key == pg.K_d:
                change_shape_triangle()
            elif event.key == pg.K_r:
                overlay_shape()
            elif event.key == pg.K_1:
                black_color()
            elif event.key == pg.K_2:
                white_color()
            elif event.key == pg.K_3:
                red_color()
            elif event.key == pg.K_4:
                orange_color()
            elif event.key == pg.K_5:
                yellow_color()
            elif event.key == pg.K_6:
                green_color()
            elif event.key == pg.K_7:
                blue_color()
            elif event.key == pg.K_8:
                purple_color()
            elif event.key == pg.K_9:
                brown_color()
            elif event.key == pg.K_0:
                player_color()
            elif event.key == pygame.K_f:
                pipet()
            # Emptying canvas:
            elif event.key == pg.K_c:
                clear_func()
            # Undoing and redoing:
            elif event.key == pg.K_q and undone < maxundone:
                undone += 1
                dirtyrects.append(screen)
            elif event.key == pg.K_e and undone > 0:
                undone -= 1
                dirtyrects.append(screen)
            # types of triangle:
            elif event.key in arrows:
                interaction_with_shapes()
            # locked coord:
            elif event.key == pg.K_x:
                locked_cord_x()
            elif event.key == pg.K_y:
                locked_cord_y()
        # Painting:
        painting()
        overlay.blit(overlaybg, screen)
        window.blit(overlay, screen)
        # sliders:
        player_color_info()
        # Updating display:
        updating()
        dirtyrects.clear()

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" plot plasma curves for the open one compartment model """

import PySimpleGUI as sg
import fin_diff as fd
import math

""" Drawing the Bateman function in PySimpleGUI """

MAX_X = 500
MAX_Y =  75

def bateman(t, params):
    D, ka, ke = params
    if ka == ke:
        return 100*ka*t*math.exp(-ka*t)
    else:
        return 100*ka/(ka - ke)*(math.exp(-ke*t) - math.exp(-ka*t))


def draw_axis():
    graph.draw_line((0, 0), (MAX_X, 0))                # axis lines # 
    graph.draw_line((0, 0), (0, MAX_Y))

    for x in range(0, MAX_X+1, 100):
        graph.draw_line((x, 0), (x, 1))                # tick marks
        if x != 0:
            # numeric labels
            graph.draw_text(str(x), (x, -2))

    for y in range(0, MAX_Y+1, 25):
        graph.draw_line((0, y), (10, y))
        if y != 0:
            graph.draw_text(str(y), (-10, y))

    graph.draw_text('t/min', (MAX_X+5, -5))
    graph.draw_text('m/mg', (-10, MAX_Y+4))
    

# Create the graph that will be put into the window
graph = sg.Graph(canvas_size=(800, 500),
                 graph_bottom_left=(-25, -6),
                 graph_top_right=(MAX_X+20, MAX_Y+8),
                 background_color='white',
                 key='graph')

# Window layout
layout = [[sg.Text('Ein-Kompartiment-Modell', font='COURIER 18')],
          [sg.Text('(extravasale Applikation)', font='COURIER 18')],
          [graph],
          
          [sg.Frame('1. Ordnung:', title_color='red', layout=[
              [sg.Text('Dosis:', size=(6,1)),
               sg.Slider((1, 200), default_value=100, size=(40,15),
                         orientation='h', enable_events=True, key='-D1-'),
               sg.Text('mg') ],
              [sg.Text('k_i:', size=(6,1)),
               sg.Slider((1, 500), default_value=300, size=(40,15),
                         orientation='h', enable_events=True, key='-K1-'),
               sg.Text('10000/min') ]])],
          [sg.Frame('0. Ordnung:', title_color='blue', layout=[
              [sg.Text('Dosis:', size=(6,1)),
               sg.Slider((1, 200), default_value=100, size=(40,15),
                         orientation='h', enable_events=True, key='-D0-'),
               sg.Text('mg') ],
              [sg.Text('k_i:', size=(6,1)),
               sg.Slider((1, 500), default_value=100, size=(40,15),
                         orientation='h', enable_events=True, key='-K0-'),
               sg.Text('100 mg/min') ]])],
          [sg.Text('k_e:', size=(6,1)),
           sg.Slider((0, 500), default_value=200, size=(40,15),
                     orientation='h', enable_events=True, key='-KE-'),
           sg.Text('10000/min')],
          [sg.Quit() ]
]

def draw_graph(values):
    graph.erase()
    draw_axis()

    dose0 = float(values['-D0-'])
    dose1 = float(values['-D1-'])
    k0 = int(values['-K0-'])/100
    k1 = int(values['-K1-'])/10000
    ke = int(values['-KE-'])/10000

    b0 = fd.Bateman_0(dose0, k0, ke, MAX_X)
    prev_x = prev_y = None
    for x in b0.index:
        y = b0.data.iloc[x, 1]
        if prev_x is not None:
            graph.draw_line((prev_x, prev_y), (x, y), color='blue')
        prev_x, prev_y = x, y

    b1 = fd.Bateman_1(dose1, k1, ke, MAX_X)
    prev_x = prev_y = None
    for x in b1.index:
        y = b1.data.iloc[x, 1]
        if prev_x is not None:
            graph.draw_line((prev_x, prev_y), (x, y), color='red')
        prev_x, prev_y = x, y

window = sg.Window('Bateman-Funktion', layout)
window.Finalize()
draw_graph({'-D0-': window['-D0-'].DefaultValue, '-D1-': window['-D1-'].DefaultValue,
            '-K0-': window['-K0-'].DefaultValue, '-K1-': window['-K1-'].DefaultValue, 
            '-KE-': window['-KE-'].DefaultValue})

while True:
    event, values = window.read()
    if event in [ None, 'Quit']:
        break

    draw_graph(values)
    
window.close()

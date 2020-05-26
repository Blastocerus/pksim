#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" plot plasma curves for the open one compartment model """

import PySimpleGUI as sg
import fin_diff as fd
import math

""" Drawing the Bateman function in PySimpleGUI """

MAX_X = 500
MAX_Y = 100

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

label_size  = ( 6,  1)
slider_size = (60, 18)

# Window layout
layout = [[sg.Text('Ein-Kompartiment-Modell', font='COURIER 18')],
          [sg.Text('(extravasale Applikation)', font='COURIER 18')],
          [graph],
          
          [sg.Frame('1. Ordnung:', title_color='blue', layout=[
              [sg.Text('Dosis:', size=label_size),
               sg.Slider((1, 200), default_value=200, size=slider_size,
                         orientation='h', enable_events=True, key='-D1-'),
               sg.Text('mg') ],
              [sg.Text('k_i:', size=label_size),
               sg.Slider((0, 500), default_value=150, size=slider_size,
                         orientation='h', enable_events=True, key='-KI1-'),
               sg.Text('10000/min')],
              [sg.Text('k_e:', size=label_size),
               sg.Slider((1, 500), default_value=300, size=slider_size,
                         orientation='h', enable_events=True, key='-KE1-'),
               sg.Text('10000/min') ]])],
          [sg.Frame('1. Ordnung:', title_color='red', layout=[
              [sg.Text('Dosis:', size=label_size),
               sg.Slider((1, 200), default_value=200, size=slider_size,
                         orientation='h', enable_events=True, key='-D2-'),
               sg.Text('mg') ],
              [sg.Text('k_i:', size=label_size),
               sg.Slider((0, 500), default_value=150, size=slider_size,
                         orientation='h', enable_events=True, key='-KI2-'),
           sg.Text('10000/min')],
              [sg.Text('k_e:', size=label_size),
               sg.Slider((1, 500), default_value=100, size=slider_size,
                         orientation='h', enable_events=True, key='-KE2-'),
               sg.Text('10000/min') ]])],
          [sg.Quit() ]
]


def plot_graph(index, values, col):
    prev_x = prev_y = None
    for x, y in zip(index, values):
        if prev_x is not None:
            graph.draw_line((prev_x, prev_y), (x, y), color=col)
        prev_x, prev_y = x, y

def draw_graph(values):
    graph.erase()
    draw_axis()

    dose2 = float(values['-D2-'])
    dose1 = float(values['-D1-'])
    ki1 = int(values['-KI1-'])/10000
    ki2 = int(values['-KI2-'])/10000
    ke1 = int(values['-KE1-'])/10000
    ke2 = int(values['-KE2-'])/10000

    b1 = fd.Bateman_1(dose1, ki1, ke1, MAX_X)
    plot_graph(b1.index, b1.data['Plasma'], 'blue')

    b2 = fd.Bateman_1(dose2, ki2, ke2, MAX_X)
    plot_graph(b2.index, b2.data['Plasma'], 'red')

window = sg.Window('Bateman-Funktion', layout)
window.Finalize()
draw_graph({'-D2-': window['-D2-'].DefaultValue, '-D1-': window['-D1-'].DefaultValue,
            '-KE2-': window['-KE2-'].DefaultValue, '-KE1-': window['-KE1-'].DefaultValue, 
            '-KI2-': window['-KI2-'].DefaultValue, '-KI1-': window['-KI1-'].DefaultValue})

while True:
    event, values = window.read()
    if event in [ None, 'Quit']:
        break

    draw_graph(values)
    
window.close()

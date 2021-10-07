from random import randint
from dearpygui.dearpygui import *

from components.ploter import Ploter

plot = Ploter


def render_controle(plots):
    for plot in plots:
        plot.update()


POINTS = 50


def init_controle(windows: dict, callback):
    with window(id=2_0, width=400, height=400, no_move=False, pos=[50, 50]) as Grafico:
        windows['Controle'].append(Grafico)
        dataset = []
        for i in range(POINTS):
            dataset.append([i, i+randint(-1, 1)])

        plot1 = Ploter(
            parent=Grafico,
            data=dataset,
            pos=[0, 0],
            size=[400, 400],
            resolution=POINTS,
            offset_x=10,
            offset_y=10,
            thickness_line=2,
            show_line=True,
            color_line='b',
            color_mark='r',
            size_mark=5,
            marker='^',
        )

    with window(id=2_1, width=500, height=250, no_move=False, pos=[500, 500]) as Grafico1:
        windows['Controle'].append(Grafico1)
        dataset = []
        for i in range(POINTS):
            dataset.append([i, i+randint(-1, 1)])

        plot2 = Ploter(
            parent=Grafico1,
            data=dataset,
            pos=[0, 0],
            size=[50, 50],
            resolution=15,
            offset_x=10,
            offset_y=10,
            thickness_line=2,
            show_line=True,
            color_line='b',
            color_mark='r',
            size_mark=5,
            marker='+',
        )
    with window(id=2_52, width=400, height=300, no_move=False, pos=[500, 150]) as Grafico2:
        windows['Controle'].append(Grafico2)
        dataset = []
        for i in range(POINTS):
            dataset.append([i, i+randint(-1, 1)])

        plot3 = Ploter(
            parent=Grafico2,
            data=dataset,
            pos=[0, 0],
            size=[50, 50],
            resolution=30,
            offset_x=20,
            offset_y=10,
            thickness_line=3,
            show_line=True,
            color_line='g',
            color_mark='b',
            size_mark=2,
            marker='o',
        )
    return [plot1, plot2, plot3]

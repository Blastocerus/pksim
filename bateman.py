#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" plot plasma curves for the open one compartment model """

import matplotlib.pyplot as plt
import fin_diff as fd

m0 = fd.Bateman_0(ki=0.3).data
m1 = fd.Bateman_1(ki=0.02).data

fig = plt.figure(figsize=(8, 5))
grid = (3, 2)


plasma_ax = plt.subplot2grid(grid, (0, 0), colspan=1, rowspan=2)
i_ax = plt.subplot2grid(grid, (0, 1))
e_ax = plt.subplot2grid(grid, (1, 1))

for ax in (plasma_ax, i_ax, e_ax):
    ax.set_xlabel('t/max')
    ax.set_ylabel('m/mg')

m0.reset_index().plot.line('index', 'Plasma', ax=plasma_ax)
m1.reset_index().plot.line('index', 'Plasma', ax=plasma_ax)

m0.reset_index().plot.line('index', 'Arzneiform', ax=i_ax)
m1.reset_index().plot.line('index', 'Arzneiform', ax=i_ax)

m0.reset_index().plot.line('index', 'Elimination', ax=e_ax)
m1.reset_index().plot.line('index', 'Elimination', ax=e_ax)

plt.savefig('bateman.png', orientation='landscape')

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" finite difference implementation of pharmacokinetical compartment models """

import numpy as np
import pandas as pd

class Dosing():
    """ dosing scheme of an API,
        or a pair of two arrays, of which the elements of the first are applied once
        and afterwards the element of the second periodically """

    def __init__(self, once, periodic):
        self.a1 = once
        self.a2 = periodic
        self.n1 = len(once)
        self.n2 = len(periodic)

    def get(self, i):
        if i < self.n1:
            return self.a1[i]
        else:
            i = i - self.n1
            return self.a2[i % self.n2]


class Bolus(Dosing):
    """ adminster a certain amount of API at once """

    def __init__(self, dose):
        Dosing.__init__(self, [dose], [0])


class Null(Bolus):
    """ no API is given """

    def __init__(self):
        Bolus.__init__(self, 0)

Nothing = Null()
            
class DoseFunction(Dosing):
    """ a function that descibes the API concentration over time """

    pass                        # not implemented yet


class Compartment():
    """ fictitious volume in which API instaniously and homogeniously distributes
        v: volume of distribution / ml
        m: mass of API /mg in the compartment
    """

    def __init__(self, name, dosing = Nothing, volume=1):
        self.name = name
        self.dosing = dosing

        self.m = None
        self.v = volume

    def reset(self, n):
        self.m = np.full(n + 1, None)
        self.m[0] = self.dosing.get(0)

    def mass(self):
        if self.m is not None:
            return pd.Series(self.m, name = self.name)
        else:
            return None

    def concentration(self):
        if self.m:
            return self.mass()/self.v
        else:
            return None


class Transition():
    """ describes the kinetcs with which an API transitions to another compartment 
    """

    def __init__(self):
        self.params = None

    def minute_diff(self, comp, t):
        """ how much API leaves a compartment per minute """
        return 0

class NullTransition(Transition):
    """ no transition """

    pass

class Order_1(Transition):
    """ first order kinetics """

    def __init__(self, k):
        self.k = k
        self.mf = 1 - np.exp(-k)

    def minute_diff(self, comp, t):
        return comp.m[t] * self.mf

class Order_0(Transition):
    """ zero order kinetics """
    
    def __init__(self, k):
        self.k = k
        
    def minute_diff(self, comp, t):
        delta_m = self.k
        mass_left = comp.m[t]
        if mass_left > delta_m:
            return delta_m
        else:
            return mass_left

class FiniteDifferenceModel:
    """ simulation of api levels in a general linear pharmacokinetical model
    """

    def __init__(self, compartments, transition_matrix, t_omega=500):
        """ transitions: n x n matrix of Transitions """

        self.C = np.array(compartments)
        self.T = np.array(transition_matrix)

        self.data = self.simulate(t_omega)

    def simulate(self, t_omega=500):
        """ simulate api levels in the compartments for t minutes """

        # initialise states
        for c in self.C:
            c.reset(t_omega)

        ## simulation
        t_series = pd.Series(range(t_omega + 1))
        for t in t_series[1:]:
            # update dose
            for c in self.C:
                c.m[t] = c.m[t-1] + c.dosing.get(t)

            # apply transition matrix
            for src, ts in zip(self.C, self.T):
                for dest, tn in zip(self.C, ts):
                    dt = tn.minute_diff(src, t)
                    src.m[t] -= dt
                    dest.m[t] += dt

        result = pd.concat([c.mass() for c in self.C], axis=1)
        result.set_index(t_series)

        return result

# simulations in an one compartment model
class OneCompartment(FiniteDifferenceModel):

    def __init__(self, dose_a, tm, t_omega):
        
        A = Compartment("Arzneiform", dose_a)
        C = Compartment("Plasma")
        E = Compartment("Elimination")

        super().__init__((A, C, E), tm, t_omega)
        
    
class Bateman_1(OneCompartment):

    def __init__(self, dose_a=Bolus(100), ki=0.04, ke=0.02, d = 100, t_omega=500):

        invasion = Order_1(ki)
        elimination = Order_1(ke)
        N = NullTransition()
        tm = [[N, invasion, N], [N, N, elimination], [N, N, N]]
        
        super().__init__(dose_a, tm, t_omega)

class Bateman_0(OneCompartment):

    def __init__(self, dose_a=Bolus(100), ki=1, ke=0.02, d = 100, t_omega=500):

        invasion = Order_0(ki)
        elimination = Order_1(ke)
        N = NullTransition()
        tm = [[N, invasion, N], [N, N, elimination], [N, N, N]]
        
        super().__init__(dose_a, tm, t_omega)



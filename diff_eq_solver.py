from numerical_method import * 
import operator
import numpy as np
import matplotlib.pyplot as plt
import math

import functools

class diff_eq_solver:
    def __init__(self, f_der, f):
        self.f_der = f_der
        self.f = f
        self.x0 = 1
        self.y0 = 1
        self.n_intervals = 10
        self.x_max = 2

    def set_initial_point(self, x0, y0):
        # Protection if new x0 > old x_max
        self.x_max = self.x_max - self.x0 + x0
        self.x0 = x0
        self.y0 = y0
    
    def set_n_intervals(self, n_intervals):
        self.n_intervals = n_intervals

    def set_x_max(self, x_max):
        self.x_max = x_max

    def set_num_method(self, nm):
        self.nm = nm

    def get_xs(self, n_intervals=None):
        if n_intervals == None:
            n_intervals = self.n_intervals
        
        return np.linspace(
            start=self.x0, 
            stop=self.x_max,
            num=n_intervals + 1
            )

    def get_exact(self, n_intervals=None):
        if n_intervals == None:
            xs = self.get_xs()
        else:
            xs = self.get_xs(n_intervals)

        return self.f(self.x0, self.y0, xs)

    def apply_method(self, n_intervals=None):
        if n_intervals == None:
            n_intervals = self.n_intervals

        step_size = (self.x_max - self.x0) / n_intervals
        xs = self.get_xs(n_intervals)

        approximation = np.zeros(n_intervals + 1)
        approximation[0] = self.y0

        for i in range(1, n_intervals + 1):
            approximation[i] = self.nm.calculate(
                xs[i - 1],
                approximation[i - 1],
                step_size,
                self.f_der
                )
        
        print(xs)
        print(approximation)

        return approximation

    def calc_lte(self, n_intervals=None):
        if n_intervals == None:
            n_intervals = self.n_intervals

        exact = self.get_exact(n_intervals)
        appr = self.apply_method(n_intervals)

        return abs(exact - appr)

    def calc_gte(self):
        n0 = 1
        ns = np.arange(n0, self.n_intervals + 2, 1)
        gte = np.zeros(self.n_intervals - n0 + 2)

        for i in range(n0, self.n_intervals + 2):
            gte[i - n0] = np.max(self.calc_lte(i))

        return (ns, gte)

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
        self.n0 = 9
        self.n_intervals = 20
        self.x_max = 2

    def set_initial_point(self, x0, y0):
        # Protection if new x0 > old x_max
        self.x_max = self.x_max - self.x0 + x0
        self.x0 = x0
        self.y0 = y0
    
    def set_n_intervals(self, n_intervals: int):
        self.n_intervals = n_intervals

    def set_n0(self, n0: int):
        self.n0 = n0

    def set_x_max(self, x_max):
        self.x_max = x_max

    def set_num_method(self, nm):
        self.nm = nm

    @staticmethod
    def _split_by_zero(arr):
        lt = arr[arr < 0]
        gt = arr[arr > 0]

        return [lt, gt]

    def get_xs(self, n_intervals=None):
        if n_intervals == None:
            n_intervals = self.n_intervals
        
        return self._split_by_zero(np.linspace(
            start=self.x0, 
            stop=self.x_max,
            num=n_intervals + 1
        ))

    def get_exact(self, n_intervals=None):
        if n_intervals == None:
            xs = self.get_xs()
        else:
            xs = self.get_xs(n_intervals)

        return list(map(
            lambda x: self.f(self.x0, self.y0, x), 
            xs
            ))

    def get_approximation(self, n_intervals=None):
        if n_intervals == None:
            n_intervals = self.n_intervals

        xs = self.get_xs(n_intervals)
        step_size = (self.x_max - self.x0) / n_intervals

        res = list(map(
            lambda x: self.apply_method(
                xs=x, 
                step_size=step_size
                ),
            xs
            ))

        return res

    def apply_method(self, xs, step_size=None):
        if step_size == None:
            step_size = (self.x_max - self.x0) / self.n_intervals

        approximation = np.zeros(xs.size)
        if xs.size != 0:
            approximation[0] = self.f(self.x0, self.y0, xs[0])

        for i in range(1, xs.size):
            approximation[i] = self.nm.calculate(
                xs[i - 1],
                approximation[i - 1],
                step_size,
                self.f_der
                )
        
        return approximation

    def calc_lte(self, n_intervals=None):
        if n_intervals == None:
            n_intervals = self.n_intervals

        exact = self.get_exact(n_intervals)
        appr = self.get_approximation(n_intervals)

        return list(map(lambda x, y: abs(x - y), exact, appr))

    def calc_gte(self):
        ns = np.arange(self.n0, self.n_intervals + 1, 1)
        gte = np.zeros(self.n_intervals - self.n0 + 1)

        for i in range(self.n0, self.n_intervals + 1):
            print('lte')
            print(self.calc_lte(i))
            print('xs')
            print(self.get_xs(i))
            gte[i - self.n0] = max(map(
                lambda x: np.amax(x, initial=0), 
                self.calc_lte(i)))

        return (ns, gte)

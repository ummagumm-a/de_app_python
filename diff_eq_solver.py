from numerical_method import * 
import operator
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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

        self.step_size = (self.x_max - self.x0) / self.n_intervals

        self.xs = np.arange(
            start=self.x0, 
            stop=self.x_max, 
            step=self.step_size
            )
            
        self.exact = self.f(self.x0, self.y0, self.xs)

    def set_initial_point(self, x0, y0):
        self.x_max = self.x_max - self.x0 + x0
        self.x0 = x0
        self.y0 = y0
        self.update_calcs()
    
    def set_n_intervals(self, n_intervals):
        self.n_intervals = n_intervals
        self.update_calcs()

    def set_x_max(self, x_max):
        self.x_max = x_max
        self.update_calcs()

    def set_num_method(self, nm):
        self.nm = nm
        self.update_calcs()

    def update_calcs(self):
        self.step_size = (self.x_max - self.x0) / self.n_intervals

        self.xs = np.arange(
            start=self.x0, 
            stop=self.x_max, 
            step=self.step_size
            )
            
        self.exact = self.f(self.x0, self.y0, self.xs)

        self.apply_method()
        self._calc_lte()
#        self._calc_gte()

    def apply_method(self):
        self.approximation = np.zeros(self.n_intervals)
        self.approximation[0] = self.y0

        for i in range(1, self.n_intervals):
            self.approximation[i] = self.nm.calculate(
                self.xs[i - 1],
                self.approximation[i - 1],
                self.step_size,
                self.f_der
                )

        return self.approximation

    def _calc_lte(self):
        self.lte = abs(self.exact - self.approximation)

    def _calc_gte(self):
        n0 = math.ceil((self.x_max - self.x0) / 0.5)
        ini_n = self.N
        ini_step_size = self.step_size
        self.data['is'] = np.arange(n0, self.N, 1)
        self.data['gte'] = np.zeros(self.N - n0)
        for i in range(n0, N):
            self.n_intervals = i
            self.step_size = (self.x_max - self.x0) / i
            self._calc_lte()
        self.data['gte'][i] = max(self.data['approximation'])

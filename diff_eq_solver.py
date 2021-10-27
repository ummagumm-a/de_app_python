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

        self.update_calcs()

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

    def update_calcs(self):
        self.step_size = (self.x_max - self.x0) / self.n_intervals

        new_data = pd.DataFrame()

        new_xs = np.arange(
            start=self.x0, 
            stop=self.x_max, 
            step=self.step_size)
            
        new_data['xs'] = new_xs
        new_data['exact'] = self.f(self.x0, self.y0, new_xs)
        print('exact')
        print(new_data['exact'])

        self.update_approximations(new_data, new_xs)
        self.data = new_data
        self._calc_lte()

    def update_approximations(self, data, xs):
        for method in num_meth_list:
            data[str(method)] = self.apply_method(method, xs)

    def apply_method(self, method, xs):
        approximation = np.zeros(self.n_intervals)
        approximation[0] = self.y0

        for i in range(1, self.n_intervals):
            approximation[i] = method.calculate(
                xs[i - 1],
                approximation[i - 1],
                self.step_size,
                self.f_der)

        return approximation

    def _calc_lte(self):
        for method in num_meth_list:
            self.data[str(method) + '_lte'] = abs(self.data['exact'] 
                                            - self.data[str(method)])

    def _calc_gte(self):
        for method in num_meth_list:
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

    # def __str__(self):
    #     return 'xs: ' + str(self.xs) + \
    #         '\nexact: ' + str(self.exact) + \
    #         '\napproximation: ' + str(self.approximation) + \
    #         '\nlte: ' + str(self.lte) + \
    #         '\ngte: ' + str(self.gte)

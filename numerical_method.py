import abc
import numpy as np

class numerical_method(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'calculate') and
                callable(subclass.calculate))

    @abc.abstractmethod
    def calculate(self, x_prev: np.float32, y_prev, step_size, f_der):
        raise NotImplementedError
    
class euler_method(numerical_method):
    def __str__(self):
        return 'euler'

    def calculate(self, x_prev, y_prev, step_size, f_der):
        return y_prev + step_size * f_der(x_prev, y_prev)
    

class improved_euler_method(numerical_method):
    def __str__(self):
        return 'impr_euler'

    def calculate(self, x_prev, y_prev, step_size, f_der):
        k1 = step_size * f_der(x_prev, y_prev)
        k2 = step_size * f_der(x_prev + step_size, y_prev + k1);
        return y_prev + (k1 + k2) / 2

class runge_kutta_method(numerical_method):
    def __str__(self):
        return 'runge_kutta'

    def calculate(self, x_prev, y_prev, step_size, f_der):
        k1 = step_size * f_der(x_prev, y_prev)
        k2 = step_size * f_der(x_prev + step_size / 2, y_prev + k1 / 2)
        k3 = step_size * f_der(x_prev + step_size / 2, y_prev + k2 / 2)
        k4 = step_size * f_der(x_prev + step_size, y_prev + k3)

        return y_prev + (k1 + 2 * k2 + 2 * k3 + k4) / 6

num_meth_list = [euler_method(), improved_euler_method(), runge_kutta_method()]
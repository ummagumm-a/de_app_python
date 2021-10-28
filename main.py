from diff_eq_solver import diff_eq_solver
from app import my_app

from math import e

des = diff_eq_solver(
    lambda x, y: (3 * y + 2 * x * y) / x ** 2,
    lambda x0, y0, x: y0 / (x0 ** 2 * e ** (-3 / x0)) * x ** 2 * e ** (-3 / x)
    )

app = my_app(des)

if __name__ == '__main__':
    app.run()
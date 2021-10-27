import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import numpy as np



class plotter:
    def __init__(self, des):

        self.des = des
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        l, = draw()

        def submit_initial(text):
            x0, y0 = text.split()
            self.des.set_initial_point(x0, y0)
            l1, = draw()
            plt.draw()

        default_initials = str(des.x0) + ' ' + str(des.y0)
        axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
        text_box = TextBox(axbox, 'Initial contitions', initial=default_initials)
        text_box.on_submit(submit_initial)
        plt.show()




            

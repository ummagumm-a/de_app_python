from numerical_method import *

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

colors = ['green', 'orange', 'cornflowerblue']
num_meth_list = [
    euler_method(), 
    improved_euler_method(), 
    runge_kutta_method()
    ]

class graph:

    def __init__(self, des):
        self.des = des

    def _methods_figure(self, fig, row, col):
        xs = self.des.get_xs()
        exact = self.des.get_exact()
        showlegend = True 
        for (x, y) in zip(xs, exact):
            fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    name="Exact Solution",
                    showlegend=showlegend,
                    marker=dict(color='black', opacity=0.0),
                    line_shape='linear'),
                row, col)
            showlegend=False

        for i in range(0, len(num_meth_list)):
            self.des.set_num_method(num_meth_list[i])
            appr = self.des.get_approximation()
            showlegend = True 
            for (x, y) in zip(xs, appr):
                fig.add_trace(go.Scatter(
                        x=x,
                        y=y,
                        name=str(num_meth_list[i]),
                        marker=dict(color=colors[i], opacity=0.0),
                        showlegend=showlegend,
                        line_shape='linear'),
                    row, col)
                showlegend=False

        fig.update_traces(showlegend=True,hoverinfo='text+name', mode='lines+markers')
        fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

    def _lte_figure(self, fig, row, col):
        xs = self.des.get_xs()
        for i in range(0, len(num_meth_list)):
            self.des.set_num_method(num_meth_list[i])
            lte = self.des.calc_lte()
            for (x, y) in zip(xs, lte):
                fig.add_trace(go.Scatter(
                        x=x,
                        y=y,
                        name=str(num_meth_list[i]),
                        marker=dict(color=colors[i], opacity=0.0),
                        line_shape='linear',
                        showlegend=False,
                        ),
                    row, col
                    )

        fig.update_traces(hoverinfo='text+name', mode='lines+markers')
        fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

    def _gte_figure(self, fig, row, col):
        for i in range(0, len(num_meth_list)):
            self.des.set_num_method(num_meth_list[i])
            ns, gte = self.des.calc_gte()
            fig.append_trace(go.Scatter(
                    x=ns,
                    y=gte,
                    name=str(num_meth_list[i]),
                    marker=dict(color=colors[i], opacity=0.0),
                    line_shape='linear',
                    showlegend=False,
                    ),
                row, col
            )

        fig.update_traces(hoverinfo='text+name', mode='lines+markers')
        fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))


    def construct_figures(self):
        fig = make_subplots(
            rows=2, cols=2, 
            specs=[[{}, {"rowspan": 2}],
                [{}, None]],
            subplot_titles=(
                "Approximations vs. Exact Solution",
                "GTE",
                "LTE",
                )
            )
        self._methods_figure(fig, 1, 1)
        self._lte_figure(fig, 2, 1)
        self._gte_figure(fig, 1, 2)

        return fig
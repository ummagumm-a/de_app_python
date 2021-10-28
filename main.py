from numerical_method import *
from diff_eq_solver import diff_eq_solver
import numpy as np

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

from math import e

colors = ['green', 'orange', 'cornflowerblue']
num_meth_list = [
    euler_method(), 
    improved_euler_method(), 
    runge_kutta_method()
    ]

def methods_figure(fig, row, col):
    xs = des.get_xs()
    exact = des.get_exact()
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
        des.set_num_method(num_meth_list[i])
        appr = des.get_approximation()
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

def lte_figure(fig, row, col):
    xs = des.get_xs()
    for i in range(0, len(num_meth_list)):
        des.set_num_method(num_meth_list[i])
        lte = des.calc_lte()
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

def gte_figure(fig, row, col):
    for i in range(0, len(num_meth_list)):
        des.set_num_method(num_meth_list[i])
        ns, gte = des.calc_gte()
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


def construct_figures():
    fig = make_subplots(
        rows=2, cols=2, 
        specs=[[{}, {"rowspan": 2}],
               [{}, None]],
        print_grid=True,
        subplot_titles=(
            "Approximations vs. Exact Solution",
            "GTE",
            "LTE",
            )
        )
    methods_figure(fig, 1, 1)
    lte_figure(fig, 2, 1)
    gte_figure(fig, 1, 2)

    return fig

app = dash.Dash(__name__)

des = diff_eq_solver(
    lambda x, y: (3 * y + 2 * x * y) / x ** 2,
    lambda x0, y0, x: y0 / (x0 ** 2 * e ** (-3 / x0)) * x ** 2 * e ** (-3 / x)
    )

des.set_num_method(euler_method())
fig = construct_figures()

app.layout = html.Div(children=[
    html.H1(children='Numerical Methods'),

    dcc.Graph(
        id='graph',
        figure=fig,
    ),

    html.Label('Initial conditions:'),
    html.Br(),
    dcc.Input(id='initials', type='text', placeholder='x0 y0'),
    html.Button(id='submit-initials', n_clicks=0, children='Submit'),
    html.Br(),

    html.Label('N0:'),
    html.Br(),
    dcc.Input(id='n0', type='text', placeholder='N0'),
    html.Button(id='submit-n0', n_clicks=0, children='Submit'),
    html.Br(),

    html.Label('N:'),
    html.Br(),
    dcc.Input(id='n_intervals', type='text', placeholder='N'),
    html.Button(id='submit-n_intervals', n_clicks=0, children='Submit'),
    html.Br(),
    
    html.Label('X:'),
    html.Br(),
    dcc.Input(id='x_max', type='text', placeholder='X'),
    html.Button(id='submit-x_max', n_clicks=0, children='Submit'),
    html.Br(),
])

@app.callback(
    Output('graph', 'figure'),
    Input('submit-initials', 'n_clicks'),
    Input('submit-n0', 'n_clicks'),
    Input('submit-n_intervals', 'n_clicks'),
    Input('submit-x_max', 'n_clicks'),
    State('initials', 'value'),
    State('n0', 'value'),
    State('n_intervals', 'value'),
    State('x_max', 'value'),
)
def accept_initials(n_clicks1, n_clicks2, n_clicks3, n_clicks4,
        initials, n0, n_intervals, x_max):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'submit-initials':
        try:
            x0, y0 = map(float, initials.split())
        except ValueError:
            x0, y0 = des.x0, des.y0
        
        des.set_initial_point(x0, y0)
    elif button_id == 'submit-n_intervals':
        try:
            n = int(n_intervals)
        except ValueError:
            n = des.n_intervals
            
        des.set_n_intervals(n)
    elif button_id == 'submit-n0':
        try:
            n = int(n0)
        except ValueError:
            n = des.n0
            
        des.set_n0(n)

    elif button_id == 'submit-x_max':
        try:
            x_max = float(x_max)
        except ValueError:
            x_max = des.x_max

        des.set_x_max(x_max)

    return construct_figures()

if __name__ == '__main__':
    app.run_server(debug=True)
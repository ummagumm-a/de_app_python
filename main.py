from numerical_method import *
from diff_eq_solver import diff_eq_solver
#%matplotlib inline
import numpy as np
from plotter import plotter

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import plotly.express as px
import pandas as pd
from math import e

colors = ['green', 'orange', 'cornflowerblue']
def methods_figure(fig, row, col):
    fig.add_trace(go.Scatter(
            x=des.data['xs'], 
            y=des.data['exact'], 
            name="exact",
            marker=dict(color='black'),
            line_shape='linear'),
        row, col)
    
    for i in range(0, len(num_meth_list)):
        fig.add_trace(go.Scatter(
                x=des.data['xs'], 
                y=des.data[str(num_meth_list[i])], 
                name=str(num_meth_list[i]),
                marker=dict(color=colors[i]),
                line_shape='linear'),
            row, col)

    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

def lte_figure(fig, row, col):
    for i in range(0, len(num_meth_list)):
        fig.append_trace(go.Scatter(
                x=des.data['xs'], 
                y=des.data[str(num_meth_list[i]) + '_lte'], 
                name=str(num_meth_list[i]),
                marker=dict(color=colors[i]),
                line_shape='linear',
                showlegend=False,
                ),
            row, col
            )

    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

def gte_figure(fig, row, col):

    for i in range(0, len(num_meth_list)):
        fig.append_trace(go.Scatter(
                x=des.data['is'], 
                y=des.data['approximation'], 
                name=str(num_meth_list[i]),
                marker=dict(color=colors[i]),
                line_shape='linear',
                showlegend=False,
                ),
            row, col
            )

    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))


def construct_figures():
    fig = make_subplots(rows=3, cols=1)
    methods_figure(fig, 1, 1)
    lte_figure(fig, 2, 1)
    gte_figure(fig, 3, 1)

    return fig

app = dash.Dash(__name__)

des = diff_eq_solver(
    lambda x, y: (3 * y + 2 * x * y) / x ** 2,
    lambda x0, y0, x: y0 / (x0 ** 2 * e ** (-3 / x0)) * x ** 2 * e ** (-3 / x)
    )

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
    Input('submit-n_intervals', 'n_clicks'),
    Input('submit-x_max', 'n_clicks'),
    State('initials', 'value'),
    State('n_intervals', 'value'),
    State('x_max', 'value'),
)
def accept_initials(n_clicks1, n_clicks2, n_clicks3, 
        initials, n_intervals, x_max):
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
    elif button_id == 'submit-x_max':
        try:
            x_max = float(x_max)
        except ValueError:
            x_max = des.x_max

        des.set_x_max(x_max)

    return construct_figures()

if __name__ == '__main__':
    app.run_server(debug=True)
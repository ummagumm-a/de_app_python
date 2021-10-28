from graph import graph
from diff_eq_solver import diff_eq_solver

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

class my_app:
    def __init__(self, des):
        self.app = dash.Dash(__name__)
        self.app.callback(
            Output('graph', 'figure'),
            Input('submit-initials', 'n_clicks'),
            Input('submit-n0', 'n_clicks'),
            Input('submit-n_intervals', 'n_clicks'),
            Input('submit-x_max', 'n_clicks'),
            State('initials', 'value'),
            State('n0', 'value'),
            State('n_intervals', 'value'),
            State('x_max', 'value'),
        )(self.callback)

        self.des = des
        self.graph_ = graph(des)
        fig = self.graph_.construct_figures()
        self.construct_layout(fig)

    def run(self):
        self.app.run_server(debug=True)

    def construct_layout(self, fig):
        self.app.layout = html.Div(children=[
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

    def callback(self, n_clicks1, n_clicks2, n_clicks3, n_clicks4,
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
                x0, y0 = self.des.x0, self.des.y0
            
            self.des.set_initial_point(x0, y0)
        elif button_id == 'submit-n_intervals':
            try:
                n = int(n_intervals)
            except ValueError:
                n = self.des.n_intervals
                
            self.des.set_n_intervals(n)
        elif button_id == 'submit-n0':
            try:
                n = int(n0)
            except ValueError:
                n = self.des.n0
                
            self.des.set_n0(n)

        elif button_id == 'submit-x_max':
            try:
                x_max = float(x_max)
            except ValueError:
                x_max = self.des.x_max

            self.des.set_x_max(x_max)

        return self.graph_.construct_figures()


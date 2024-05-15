import dash
from dash import dcc, html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import model as modelo
import numpy as np
from dash.dependencies import Input, Output


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR], use_pages=True)

app.layout = html.Div(
    [
        html.Div([
                html.Br(),
                html.H1('CSL Tech', style = {'top-padding': 40, 'text-align': 'center'}),
            ],className= ''),

        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ], style = {'text-align':'center'}),
        html.Hr(),


        dash.page_container
    ]
)

from pages.modelp import layout, register_callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash import dcc, html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import model as modelo
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div(
    [
        html.Div([
                html.H6(''),
                html.H1('  CSL Tech'),
            ],className= 'titulos', style={'fontSize':50, 'textAlign':'left', 'padding-left': 20}),

        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ]),
        html.Hr(),


        dash.page_container
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
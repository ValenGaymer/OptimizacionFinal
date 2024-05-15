import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__)

df = px.data.tips()

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)
 
layout = html.Div(
    [html.H1('kie'),
    html.Div([dcc.Input(
            id="input_{}".format('text'),
            type='text',
            placeholder="input type {}".format('text'),
        ), html.Br(),
    dcc.Input(
            id="input_{}".format('number'),
            type='number',
            placeholder="input type {}".format('number'),
        )]
    )
    ]
)

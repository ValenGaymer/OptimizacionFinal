import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR], use_pages=True, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    html.Br(),
    html.P("V2 Solutions", className="text-dark text-center fw-bold fs-1"),
    html.Div(children=[
        dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5")\
            for page in dash.page_registry.values()
    ],
    style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'justifyContent': 'center'},
    id='main-container', ),
    
    dash.page_container
], className="col-8 mx-auto")

app.title = 'V2Solutions'

# Importa tus páginas y registra callbacks
from pages.Datos import layout, register_callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)

import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output, State

dash.register_page(__name__)

 
layout = html.Div(
    [
        html.H1('Actualización del modelo'),
        html.H5('Por favor, rellene todos los campos correctamente', className='text-secondary-emphasis'),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.H4('Datos principales'),
                        html.Div(
                            [
                                html.H6('Pago de trabajadores experimentados: ', className='form-label mt-4'),
                                dcc.Input(
                                    id='input-experimentados',
                                    type='number',
                                    placeholder='Ingrese',
                                    className='input-group-text'
                                )
                            ]
                        ),
                        html.Div(
                            [
                                html.H6('Pago de trabajadores en entrenamiento: ', className='form-label mt-4'),
                                dcc.Input(
                                    id='input-entrenamiento',
                                    type='number',
                                    placeholder='Ingrese',
                                    className='input-group-text'
                                )
                            ]
                        ),
                        html.Div(
                            [
                                html.H6('Número de meses: ', className='form-label mt-4'),
                                dcc.Input(
                                    id='input-meses',
                                    type='number',
                                    placeholder='Ingrese',
                                    className='input-group-text'
                                )
                            ]
                        ),
                        html.Br(),
                        html.Button('Confirmar', id='btn-confirmar', className='btn btn-primary')
                    ],
                    style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}
                ),
                html.Div(
                    [
                        html.H4('Datos Ingresados'),
                        html.Ul(id='lista-datos')
                    ],
                    style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '20px'}
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                html.H4('Restricciones')
            ]
        )
    ],
    style={'padding': 5}
)

def register_callbacks(app):
    @app.callback(
        Output('lista-datos', 'children'),
        Input('btn-confirmar', 'n_clicks'),
        State('input-experimentados', 'value'),
        State('input-entrenamiento', 'value'),
        State('input-meses', 'value')
    )
    def actualizar_datos(n_clicks, experimentados, entrenamiento, meses):
        if n_clicks is None:
            return []
        datos = [
            html.Li(f'Pago de trabajadores experimentados: {experimentados}', 
                    className = 'card border-primary mb-3', style = {'max-width': 380}),
            html.Li(f'Pago de trabajadores en entrenamiento: {entrenamiento}', 
                    className = 'card border-primary mb-3', style = {'max-width': 380}),
            html.Li(f'Número de meses: {meses}', 
                    className = 'card border-primary mb-3', style = {'max-width': 380})
        ]
        return datos
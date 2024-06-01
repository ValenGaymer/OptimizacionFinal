import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output, State

dash.register_page(__name__, path='/', name="Datos")

meses_tx = ['enero', 'febrero', 'marzo', 'abril', 
         'mayo', 'junio', 'julio', 'agosto', 
         'septiembre', 'octubre', 'noviembre', 'diciembre']
 
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
                        html.Div(
                            [
                                html.H6('Tasa de abandono de trabajadores: ', className='form-label mt-4'),
                                dcc.Input(
                                    id='input-tasa',
                                    type='number',
                                    placeholder='Ingrese',
                                    className='input-group-text'
                                )
                            ]
                        ),
                        html.Div(
                            [
                                html.H6('Trabajadores experimentados iniciales: ', className='form-label mt-4'),
                                dcc.Input(
                                    id='input-expi',
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
                    style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding-left': '20px'}
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                html.H4('Restricciones'),
                html.Div(id='meses-container')
            ]
        )
    ],
    style={'padding-left': '20px'}
)

def register_callbacks(app):

    @app.callback(
        Output('lista-datos', 'children'),
        Input('btn-confirmar', 'n_clicks'),
        State('input-experimentados', 'value'),
        State('input-entrenamiento', 'value'),
        State('input-meses', 'value'),
        State('input-tasa', 'value'),
        State('input-expi', 'value')
    )

    def actualizar_iniciales(n_clicks, experimentados, entrenamiento, meses, tasa, expi):
        if n_clicks is None:
            return []
        
        if experimentados is None:
            return[html.Li(f'Por favor, rellene todos los campos. ', 
                    className = 'card border-warning mb-3', style = {'max-width': 380, 'text-align':'center', 'padding':10})]
        
        datos = [
            html.Li(f' Pago de trabajadores experimentados: {experimentados}', 
                    className = 'card border-warning mb-3', style = {'max-width': 380, 'text-align':'center', 'padding':10}),
            html.Li(f'Pago de trabajadores en entrenamiento: {entrenamiento}', 
                    className = 'card text-white bg-warning mb-3', style = {'max-width': 380, 'text-align':'center', 'padding':10}),
            html.Li(f'Número de meses: {meses}', 
                    className = 'card border-warning mb-3', style = {'max-width': 380, 'text-align':'center', 'padding':10}),
            html.Li(f'Tasa de abandono: {tasa}', 
                    className = 'card text-white bg-warning mb-3', style = {'max-width': 380, 'text-align':'center', 'padding':10}),
            html.Li(f'Trabajadores experimentados iniciales: {expi}', 
                    className = 'card border-warning mb-3', style = {'max-width': 380, 'text-align':'center', 'padding':10})
        ]

        datamodel = [experimentados, entrenamiento, meses, tasa, expi]
        return datos
    
    @app.callback(
        Output('meses-container', 'children'),
        Input('btn-confirmar', 'n_clicks'),
        State('input-meses', 'value')
    )
    def generar_inputs_rest(n_clicks, meses):
        if meses is None or meses <= 0:
            return []
        
        if meses > 12:
            return html.H6('Meses inválidos. Ingrese un valor entre 1 y 12. ', className = 'badge rounded-pill bg-warning')

        inputs = []
        for i in range(meses):
            inputs.append(
                html.Div(
                    [
                        html.H6(f'Restricción de horas necesarias para el mes {i + 1}: ', className='form-label mt-4'),
                        dcc.Input(
                            id=f'input-mes-{i + 1}',
                            type='text',
                            placeholder=f'Ingrese datos para el mes {i + 1}',
                            className='input-group-text'
                        ),
                        dcc.Dropdown(
                            id=f'dropdown-mes-{i + 1}',
                            options=[
                                {'label': 'Mínimas', 'value': 'minimas'},
                                {'label': 'Máximas', 'value': 'maximas'}
                            ],
                            placeholder='Restricción',
                            className='input-group-text',
                            style = {'max-width': 218.4}
                        )
                    ],
                    style={'marginBottom': '10px'}
                )
            )
        
        return inputs

    
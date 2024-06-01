import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.dependencies import ALL

dash.register_page(__name__)

global meses_tx

meses_u = 0

meses_tx = ['enero', 'febrero', 'marzo', 'abril', 
            'mayo', 'junio', 'julio', 'agosto', 
            'septiembre', 'octubre', 'noviembre', 'diciembre']

datamodel = [0,0,0,0,0]

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
                                html.H6('Mayor o igual que cero', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
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
                                html.H6('Mayor o igual que cero', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
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
                                html.H6('Entre 1 y 12', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
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
                                html.H6('Entre 0 y 1', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
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
                                html.H6('Mayor o igual que cero', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
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
        ),
        html.Div(id='btn-modelo-container', style={'display': 'none'}, children=[
            html.Button('Generar modelo', id='btn-modelo', className='btn btn-primary')
        ]),
        dcc.Store(id='store-meses'),
        html.Div([html.H6('Recibió datos')], id='hold', style={'display': 'none'})
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

        global datamodel

        if n_clicks is None:
            return []
        
        # Campos vacíos
        if experimentados is None or entrenamiento is None or meses is None or tasa is None or expi is None:
            return [html.Li('Por favor, rellene todos los campos.', 
                            className='card border-warning mb-3', style={'max-width': 380, 'text-align':'center', 'padding':10})]
        
        # Campos mal puestos
        if float(tasa) >= 1 or float(tasa) <= 0:
            return [html.Li('Campo mal ingresado', 
                            className='card border-warning mb-3', style={'max-width': 380, 'text-align':'center', 'padding':10})]
        
        datos = [
            html.Li(f'Pago de trabajadores experimentados: {experimentados}', 
                    className='card border-warning mb-3', style={'max-width': 380, 'text-align':'center', 'padding':10}),
            html.Li(f'Pago de trabajadores en entrenamiento: {entrenamiento}', 
                    className='card text-white bg-warning mb-3', style={'max-width': 380, 'text-align':'center', 'padding':10}),
            html.Li(f'Número de meses: {meses}', 
                    className='card border-warning mb-3', style={'max-width': 380, 'text-align':'center', 'padding':10}),
            html.Li(f'Tasa de abandono: {tasa}', 
                    className='card text-white bg-warning mb-3', style={'max-width': 380, 'text-align':'center', 'padding':10}),
            html.Li(f'Trabajadores experimentados iniciales: {expi}', 
                    className='card border-warning mb-3', style={'max-width': 380, 'text-align':'center', 'padding':10})
        ]

        datamodel = [experimentados, entrenamiento, meses, tasa, expi]
        return datos
    
    @app.callback(
        Output('meses-container', 'children'),
        Input('btn-confirmar', 'n_clicks'),
        State('input-meses', 'value')
    )
    def generar_inputs_rest(n_clicks, meses):
        print(datamodel)

        if meses is None or meses <= 0:
            return []
        
        if meses > 12:
            return html.H6('Meses inválidos. Ingrese un valor entre 1 y 12.', className='badge rounded-pill bg-warning')

        inputs = []
        global meses_u
        meses_u = 0
        for i in range(meses):
            inputs.append(
                html.Div(
                    [
                        html.H6(f'Restricción de horas necesarias para {meses_tx[i]}: ', className='form-label mt-4'),
                        dcc.Input(
                            id=f'input-mes-{i + 1}',
                            type='number',
                            placeholder=f'Ingrese horas mínimas',
                            className='input-group-text'
                        )
                    ],
                    style={'marginBottom': '10px'}
                )
            )
            meses_u=i+1
        
        return inputs

    @app.callback(
    Output('store-meses', 'data'),
    Input('btn-modelo', 'n_clicks'),
    State('input-meses', 'value')
    )

    def update_store_meses(n_clicks, meses):
        if n_clicks is None or meses is None:
            return []

        meses_data = []

        print(dash.callback_context.triggered)
        print(dash.callback_context.inputs)
        print(dash.callback_context.states)

        for i in range(1, meses + 1):
            input_id = f'input-mes-{i}'
            input_value = dash.callback_context.states.get(input_id, {}).get('value', None)
            print(dash.callback_context.states.get(input_id, {}))
            print(f"Valor de {input_id}: {input_value}")
            meses_data.append(input_value)

        return meses_data

    
    @app.callback(
        Output('btn-modelo-container', 'style'),
        Input('btn-confirmar', 'n_clicks')
    )
    def mostrar_btn_modelo(n_clicks):
        if n_clicks is None or datamodel == []:
            return {'display': 'none'}
        
        return {'display': 'block'}

    @app.callback(
    Output('hold', 'style'),
    Input('btn-modelo', 'n_clicks'),
    State('store-meses', 'data'),
    State('input-meses', 'value'),
    prevent_initial_call=True,
    running=[(Output("btn-modelo", "disabled"), True, False)]
    )
    def modelo(n_clicks, meses_data, meses):
        if n_clicks is None:
            return {'display': 'none'}

        if len(meses_data) != meses:
            return {'display': 'none'}

        print("Valores de los meses:", meses_data)

        return {'display': 'block'}
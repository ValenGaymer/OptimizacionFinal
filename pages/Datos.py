import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.dependencies import ALL

dash.register_page(__name__)

global meses_tx


mes_act = 0

meses_u = 0

restm = []

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
                        html.Ul(id='lista-datos', className = 'list-group')
                    ],
                    style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding-left': '20px'}
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                html.H4('Restricciones'),
                html.Div(id = 'n-rest'),
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
                            className='list-group-item list-group-item-danger d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10})]
        
        # Campos mal puestos
        if float(tasa) >= 1 or float(tasa) <= 0:
            return [html.Li('Campo mal ingresado', 
                            className='list-group-item list-group-item-danger d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10})]
        
        datos = [
            html.Li(f'Pago de trabajadores experimentados: {experimentados}', 
                    className='list-group-item d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10}),
            html.Li(f'Pago de trabajadores en entrenamiento: {entrenamiento}', 
                    className='list-group-item d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10}),
            html.Li(f'Número de meses: {meses}', 
                    className='list-group-item d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10}),
            html.Li(f'Tasa de abandono: {tasa}', 
                    className='list-group-item d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10}),
            html.Li(f'Trabajadores experimentados iniciales: {expi}', 
                    className='list-group-item d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10})
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
        
        return html.Div(
                    [
                        dcc.Input(
                            id=f'input-mes',
                            type='number',
                            placeholder=f'Ingrese horas mínimas',
                            className='input-group-text'
                        ),
                        html.Button('Siguiente restricción', id='btn-rest', className='btn btn-primary')

                    ],
                    style={'marginBottom': '10px'}
                )


    
    @app.callback(
        Output('btn-modelo-container', 'style'),
        Input('btn-rest', 'n_clicks')
    )
    def mostrar_btn_modelo(n_clicks):
        global mes_act

        if mes_act == datamodel[2] + 1:
            mes_act = 0
            return {'display': 'block'}
        
        return {'display': 'none'}
    

    
    @app.callback(
        Output('n-rest', 'children'),
        Input('btn-rest', 'n_clicks'),
        Input('btn-confirmar', 'n_clicks'),
        State('input-mes','value'),
        prevent_initial_callback = True
    )

    def confirmar_modelo(n1, n2, mes):
        global mes_act
        global restm

        triggered_id = dash.ctx.triggered_id
        print(mes_act)
        print(triggered_id)
        
        if triggered_id == 'btn-rest'  and mes_act < datamodel[2]:
            if mes_act != 0:
                restm.append(mes)
                print('guardó primer if: ',restm)
            mes_act = mes_act + 1
            return html.H6(f'Restricción para el mes de {meses_tx[mes_act - 1]}')
        
        if triggered_id == 'btn-rest' and mes_act == datamodel[2]:
            mes_act = mes_act + 1
            restm.append(mes)
            print('guardó segundo if: ',restm)
            return html.H6(f'Restricción completadas')

    @app.callback(
            Output('btn-rest', 'style'),
            Input('btn-rest', 'n_clicks')
        )
    def mostrar_btn_modelo(n_clicks):
            global mes_act
            print(mes_act == datamodel[2] + 1)
            if mes_act == datamodel[2] + 1:
                return {'display': 'none'}
            
            return {'display': 'block'}  
        
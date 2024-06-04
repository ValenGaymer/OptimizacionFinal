import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.dependencies import ALL
from pulp import LpMinimize, LpProblem, LpVariable, LpInteger
import pandas as pd
import csv

app = dash.Dash(__name__)
dash.register_page(__name__)

global meses_tx
global campos_llenos
mes_act = 0
campos_llenos = False

restm = []

meses_tx = ['enero', 'febrero', 'marzo', 'abril', 
            'mayo', 'junio', 'julio', 'agosto', 
            'septiembre', 'octubre', 'noviembre', 'diciembre']

datamodel = [0,0,12,0,0,0,0]

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
                                html.H6('Mayor que cero', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
                                dcc.Input(
                                    id='input-experimentados',
                                    type='number',
                                    min = '1',
                                    placeholder='Ingrese',
                                    className='input-group-text'
                                )
                            ]
                        ),
                        html.Div(
                            [
                                html.H6('Pago de trabajadores en entrenamiento: ', className='form-label mt-4'),
                                html.H6('Mayor que cero', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
                                dcc.Input(
                                    id='input-entrenamiento',
                                    type='number',
                                    min = '1',
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
                                    min = '1',
                                    step = '1',
                                    placeholder='Ingrese',
                                    className='input-group-text'
                                ),
                                html.Div(id='output-div') 
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
                                html.H6('Mayor que cero', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
                                dcc.Input(
                                    id='input-expi',
                                    type='number',
                                    min = '1',
                                    step = '1',
                                    placeholder='Ingrese',
                                    className='input-group-text'
                                )
                            ]
                        ),
                        html.Div(
                            [
                                html.H6('Máximo de horas mensuales trabajadas: ', className='form-label mt-4'),
                                html.H6('Mayor que cero', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
                                dcc.Input(
                                    id='input-htrab',
                                    type='number',
                                    min = '1',
                                    step = '1',
                                    placeholder='Ingrese',
                                    className='input-group-text'
                                )
                            ]
                        ),
                        html.Div(
                            [
                                html.H6('Horas de entrenamiento: ', className='form-label mt-4'),
                                html.H6('Mayor que cero', className='text-secondary-emphasis', style={'font-size':'12px', 'padding-left':'9px'}),
                                dcc.Input(
                                    id='input-hent',
                                    type='number',
                                    min = '1',
                                    step = '1',
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
                html.Div(
                    [
                        dcc.Input(
                            id=f'input-mes',
                            type='number',
                            placeholder=f'Ingrese horas mínimas',
                            className='input-group-text'
                        ),
                        html.Button('Enviar restricción', id='btn-rest', className='btn btn-primary')

                    ]
                , id='meses-container', style = {'display': 'none'})
            ]
        ),
        html.Div(id='btn-modelo-container', style={'display': 'none'}, children=[
            html.Button('Generar modelo', id='btn-modelo', className='btn btn-primary')
        ]),
        html.Div(id='hold')
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
        State('input-expi', 'value'),
        State('input-htrab', 'value'),
        State('input-hent', 'value'),
        prevent_initial_callback = True
    )
    def actualizar_iniciales(n_clicks, experimentados, entrenamiento, meses, tasa, expi,htrab,hent):
        global campos_llenos
        global datamodel
        global mes_act
        mes_act = 0 

        if n_clicks is None:
            return []
        
        # Campos vacíos
        if experimentados is None or entrenamiento is None or meses is None or tasa is None or expi is None or htrab is None or hent is None:
            return [html.Li('Por favor, rellene todos los campos.', 
                            className='list-group-item list-group-item-danger d-flex justify-content-between align-items-center', 
                            style={'text-align':'center', 'padding':10})]
        
        # Campos mal puestos
        if float(tasa) >= 1 or float(tasa) <= 0:
            return [html.Li('Tasa de abandono no válida', 
                            className='list-group-item list-group-item-danger d-flex justify-content-between align-items-center', 
                            style={'text-align':'center', 'padding':10})]
        
        if int(meses) >= 13 or int(meses) <= 0:
            return [html.Li('Número de meses no válido', 
                            className='list-group-item list-group-item-danger d-flex justify-content-between align-items-center', 
                            style={'text-align':'center', 'padding':10})]
        
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
                    className='list-group-item d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10}),
            html.Li(f'Máximo de horas trabajadas por mes: {htrab}', 
                    className='list-group-item d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10}),
            html.Li(f'Horas de entrenamiento: {hent}', 
                    className='list-group-item d-flex justify-content-between align-items-center', style={'text-align':'center', 'padding':10})
        ]

        datamodel = [experimentados, entrenamiento, meses, tasa, expi, htrab, hent]
        campos_llenos = True
        return datos
    
    @app.callback(
        Output('meses-container', 'style'),
        Input('btn-confirmar', 'n_clicks'),
        State('input-meses', 'value'),
        prevent_initial_callback = True
    )
    def generar_inputs_rest(n_clicks, meses):
        if meses is None or meses <= 0 or meses > 12:
            return {'display': 'none'}
        else:
            global restm
            restm = []
            return {'display': 'block', 'marginBottom': '10px'}
    
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
        print(restm)
        print(triggered_id)

        if triggered_id == 'btn-confirmar':
            mes_act = mes_act + 1
            return html.H6(f'Restricción para el mes de enero')
        
        if triggered_id == 'btn-rest'  and mes_act < datamodel[2] and mes is not None:
            if mes_act != 0:
                restm.append(mes)
                print('guardó primer if: ',restm)
            mes_act = mes_act + 1
            return html.H6(f'Restricción para el mes de {meses_tx[mes_act - 1]}')
        
        if triggered_id == 'btn-rest' and mes_act == datamodel[2] and mes is not None:
            mes_act = mes_act + 1
            restm.append(mes)
            print('guardó segundo if: ',restm)
            return html.H6(f'Restricción completadas')
        
        if triggered_id == 'btn-rest' and mes is None:
            print('No metió nada')
            return html.H6(f'Restricción para el mes de {meses_tx[mes_act - 1]}')

    @app.callback(
            Output('btn-rest', 'style'),
            Input('btn-rest', 'n_clicks'),
            prevent_initial_callback = True
        )
    def mostrar_btn_modelo(n_clicks):
            global mes_act
            global datamodel
            if mes_act == datamodel[2] + 1:
                return {'display': 'none'}
            
            return {'display': 'block'}
    
    @app.callback(
            Output('btn-modelo-container', 'style'),
            Input('btn-rest', 'n_clicks'),
            prevent_initial_callback = True
        )
    def mostrar_btn_modelo(n_clicks):
            global mes_act
            global datamodel
            print('mostrar_btn_modelo',mes_act, datamodel)
            print(mes_act == datamodel[2] + 1)

            if mes_act == datamodel[2] + 1:
                print('Aparece btn modelo')
                return {'display': 'block'}
            
            return {'display': 'none'}
    
    @app.callback(
        Output('hold','children'),
        Input('btn-modelo','n_clicks'),
        prevent_initial_callback = True
        )

    def mostrar_btn_modelo(n_clicks):
        global datamodel
        global meses_tx
        global restm
        global mes_act
        global campos_llenos
        campos_llenos = False

        resultado = []
        if mes_act!= 0:
            resultado = [html.Br(), html.Br(), html.H5('Restricciones ingresadas: '), html.Br(),html.Br()]

            for i in range(datamodel[2]):
                resultado.append(html.H6(f'Horas mínimas para el mes de {meses_tx[i]}:  {restm[i]}', className= 'text-body-secondary'))
        
        modelito = model()
        try:
            if modelito.status == -1:
                resultado.append(html.H6(f'El modelo no es factible. Por favor, intente con restricciones diferentes. Puede ver los resultados del modelo, no son exactos.', className= 'text-danger', style = {'align':'center'}))
        except:
            pass
        return resultado

func = LpProblem("Problema", LpMinimize)
x1 = LpVariable("x1", lowBound=0, cat=LpInteger)
x2 = LpVariable("x2", lowBound=0, cat=LpInteger)
x3 = LpVariable("x3", lowBound=0, cat=LpInteger)
x4 = LpVariable("x4", lowBound=0, cat=LpInteger)
x5 = LpVariable("x5", lowBound=0, cat=LpInteger)
x6 = LpVariable("x6", lowBound=0, cat=LpInteger)
x7 = LpVariable("x7", lowBound=0, cat=LpInteger)
x8 = LpVariable("x8", lowBound=0, cat=LpInteger)
x9 = LpVariable("x9", lowBound=0, cat=LpInteger)
x10 = LpVariable("x10", lowBound=0, cat=LpInteger)
x11 = LpVariable("x11", lowBound=0, cat=LpInteger)
x12 = LpVariable("x12", lowBound=0, cat=LpInteger)

y1 = LpVariable("y1", lowBound=0, cat=LpInteger)
y2 = LpVariable("y2", lowBound=0, cat=LpInteger)
y3 = LpVariable("y3", lowBound=0, cat=LpInteger)
y4 = LpVariable("y4", lowBound=0, cat=LpInteger)
y5 = LpVariable("y5", lowBound=0, cat=LpInteger)
y6 = LpVariable("y6", lowBound=0, cat=LpInteger)
y7 = LpVariable("y7", lowBound=0, cat=LpInteger)
y8 = LpVariable("y8", lowBound=0, cat=LpInteger)
y9 = LpVariable("y9", lowBound=0, cat=LpInteger)
y10 = LpVariable("y10", lowBound=0, cat=LpInteger)
y11 = LpVariable("y11", lowBound=0, cat=LpInteger)
y12 = LpVariable("y12", lowBound=0, cat=LpInteger)

global varx
varx = [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12]

global vary
vary = [y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12]

def model():
    global func
    func =  LpProblem("Problema", LpMinimize)
    global varx
    global vary
    global datamodel
    global restm

    exp1 = 0
    exp2 = 0

    if datamodel == [0,0,12,0,0,0,0]:
        datamodel = [2000,1000,5,0.1,50,160,50]
        restm = [6000,7000,8000,9500,11000]

    for i in range(datamodel[2]):
        exp1 += varx[i]

    for i in range(datamodel[2]):
        exp2 += vary[i]

    func += datamodel[0]*(exp1) + datamodel[1]*(exp2), "Función objetivo"
    try:
        for i in range(datamodel[2]):
            func += datamodel[5]*varx[i] - datamodel[6]*vary[i] >= restm[i], f'C{i}'

        func += x1 == datamodel[4], 'CF'

        for i in range(datamodel[2] - 1):
            func += varx[i + 1] == varx[i]*(1 - datamodel[3]) + vary[i], f'R{i}'

        func.solve()
        vars = []
        for i in range(datamodel[2]):
            vars.append(varx[i].value())

        for i in range(datamodel[2]):
            vars.append(vary[i].value())

        costos = [datamodel[0],datamodel[1]]
        while len(costos)!= len(vars):
            costos.append(0)

        df = pd.DataFrame({'variables':vars, 'costos':costos})
        df.to_csv('varsmod.csv')
        print(func.status)
        print(func.objective)

        return func
    except:
        pass
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import model as modelo
import numpy as np

dash.register_page(__name__, path='/')

vars, func = modelo.model()

x_values = [1,2,3,4,5]

y1_values = vars[0:int(len(vars)/2)]
y2_values = vars[int(len(vars)/2):]

y3_values = []
for i in range(len(x_values)):
    y3_values.append(2000*y1_values[i] + 1000*y2_values[i])

print(y1_values, y2_values, y3_values)

layout = dbc.Container([
    html.Br(), 
    dbc.Row([dbc.Col(
        html.H4('Titulo1', style = {'text-align':'center'})
    ), 
    dbc.Col(
        html.H4('Titulo2', style = {'text-align':'center'})
    )]),        
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='graph1',
                figure={
                    'data': [
                        go.Scatter(
                            x=x_values,
                            y=y1_values,
                            mode='lines',
                            name='Experimentados'
                        ),
                        go.Scatter(
                            x=x_values,
                            y=y2_values,
                            mode='lines',
                            name='En entrenamiento'
                        )
                    ],
                    'layout': go.Layout(
                        height=390
                    )
                }
            ), 
            width=6
        ),

        dbc.Col(
            dcc.Graph(
                id='graph2',
                figure={
                    'data': [
                        go.Scatter(
                            x=x_values,
                            y=y3_values,
                            mode='lines',
                            name='Variable 2'
                        )
                    ],
                    'layout': go.Layout(
                        height = 390
                    )
                }
            ),
            width=6
        )
    ]),
    
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6('Trabajadores actuales'),
                html.H4(f'61')

            ], className='text-center')
        ),
        
        dbc.Col(
            html.Div([
                html.H6('Total trabajadores'),
                html.H4(f'{int(vars[1] + sum(vars[int(len(vars)/2):]))}')
            ], className='text-center')
        ),
        
        dbc.Col(
            html.Div([
                html.H6('Costo'),
                html.H4(f'${int(sum(y3_values))}')
            ], className='text-center')
        ),
        
        dbc.Col(
            html.Div([
                html.H6('Costo experimentados', className = 'card-header'),
                html.H4(f'${int(sum(y1_values)*2000)}', className = 'card-body')
            ], className = 'card text-white bg-primary mb-3', style = {'text-align':'center'})
        ),

        dbc.Col(
            html.Div([
                html.H6('Costo entrenamiento'),
                html.H4(f'${int(sum(y2_values)*1000)}')

            ], className='text-center')
        )
    ], className='mt-4')
], fluid=True)

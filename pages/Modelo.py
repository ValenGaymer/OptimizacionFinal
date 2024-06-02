import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import model as modelo
import numpy as np
from Datos import datamodel, meses_tx


app = dash.Dash(__name__)
dash.register_page(__name__, path='/', name="Modelo")

vars, func = modelo.model()

x_values = []
for i in range(len(datamodel[2])):
    x_values.append(meses_tx[i])



y1_values = vars[0:int(len(vars)/2)]
y2_values = vars[int(len(vars)/2):]

y3_values = []
for i in range(len(x_values)):
    y3_values.append(2000*y1_values[i] + 1000*y2_values[i])
    
y4_values = []
for i in range(len(x_values)):
    y4_values.append(2000*y1_values[i])
y5_values = []
for i in range(len(x_values)):
    y5_values.append(1000*y2_values[i])
    


print(y1_values, y2_values, y3_values)

layout = dbc.Container([
    html.Br(), 
    dbc.Row([dbc.Col(
        html.H4('Cantidad de trabajadores por mes', style = {'text-align':'center'})
    ), 
    dbc.Col(
        html.H4('Nómina mensual de trabajadores', style = {'text-align':'center'})
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
                            name='Experimentados',
                            line ={'color': '#ffc107'}
                        ),
                        go.Scatter(
                            x=x_values,
                            y=y2_values,
                            mode='lines',
                            name='En entrenamiento'
                        )
                    ],
                    'layout': go.Layout(
                height=390,
                plot_bgcolor='#f8f9fa',  
                paper_bgcolor='#ffffff',  
                margin={'t': 40, 'b': 40, 'l': 40, 'r': 40},  
                xaxis={'title': 'Mes'},  
                yaxis={'title': 'Cantidad de trabajadores'}, 
                legend={'x': 0.5, 'y': 1.1, 'bgcolor': '#ffffff', 'bordercolor': '#cccccc', 'borderwidth': 1},  
                showlegend=True  
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
                            name='Grupo total'
                            
                        ),
                        go.Scatter(
                            x=x_values,
                            y=y4_values,
                            mode='lines',
                            name='Experimentados'    
                        ),
                        go.Scatter(
                            x=x_values,
                            y=y5_values,
                            mode='lines',
                            name='En entrenamiento'  
                        )
                    ],
                     'layout': go.Layout(
                height=390,
                plot_bgcolor='#f8f9fa',  
                paper_bgcolor='#ffffff',  
                margin={'t': 40, 'b': 40, 'l': 40, 'r': 40},  
                xaxis={'title': 'Mes'},  
                yaxis={'title': 'Nómina'}, 
                legend={'x': 0.5, 'y': 1.1, 'bgcolor': '#ffffff', 'bordercolor': '#cccccc', 'borderwidth': 1},  
                showlegend=True  
                     )
                }
            
            ),
            width=6
        )
    ]),
    
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6('Trabajadores actuales', className = 'card-header', style={'text-align':'center', 'height': '4rem'}),
                html.H4(f'61', className = 'card-body'),

            ], className='card text-white bg-primary mb-3', style = {'text-align':'center', 'width': '12rem', 'height': '7rem'} ), align='center'
        ),
        
        dbc.Col(
            html.Div([
                html.H6('Total trabajadores', className ='card-header', style={'text-align':'center', 'height': '4rem'} ),
                html.H4(f'{int(vars[1] + sum(vars[int(len(vars)/2):]))}',className = 'card-body')
            ], className='card text-white bg-primary mb-3', style = {'text-align':'center', 'width': '12rem', 'height': '7rem'} ), align='center'
        ),
        
        dbc.Col(
            html.Div([
                html.H6('Costo', className = 'card-header', style={'text-align':'center', 'height': '4rem'}),
                html.H4(f'${int(sum(y3_values))}', className = 'card-body')
            ], className='card text-white bg-primary mb-3', style = {'text-align':'center', 'width': '12rem', 'height': '7rem'} ), align='center'
        ),
        
        dbc.Col(
            html.Div([
                html.H6('Costo experimentados', className = 'card-header', style={'text-align':'center', 'height': '4rem'}),
                html.H4(f'${int(sum(y1_values)*2000)}', className = 'card-body')
            ], className = 'card text-white bg-primary mb-3', style = {'text-align':'center', 'width': '12rem', 'height': '7rem'} ), align='center'
        ),

        dbc.Col(
            html.Div([
                html.H6('Costo entrenamiento', className='card-header', style={'text-align':'center', 'height': '4rem'}),
                html.H4(f'${int(sum(y2_values)*1000)}', className ='card-body')

            ], className='card text-white bg-primary mb-3', style = {'text-align':'center', 'width': '12rem', 'height': '7rem'} ), align='center'
        )
    ], className='mt-4')
], fluid=True)

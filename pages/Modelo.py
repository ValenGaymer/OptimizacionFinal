import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import model as modelo
import numpy as np
import csv
import pandas as pd
from dash.dependencies import Input, Output, State

meses_tx = ['enero', 'febrero', 'marzo', 'abril', 
            'mayo', 'junio', 'julio', 'agosto', 
            'septiembre', 'octubre', 'noviembre', 'diciembre']

dash.register_page(__name__, path='/', name="Modelo")

def cargar_datos():
    file = pd.read_csv('varsmod.csv')

    vars = file['variables'].tolist()
    costos = file['costos'].tolist()

    x_values = meses_tx[:int(len(vars)/2)]
    y1_values = vars[0:int(len(vars)/2)]
    y2_values = vars[int(len(vars)/2):]

    y3_values = [costos[0]*y1 + costos[1]*y2 for y1, y2 in zip(y1_values, y2_values)]
    y4_values = [costos[0]*y1 for y1 in y1_values]
    y5_values = [costos[1]*y2 for y2 in y2_values]


    return x_values, y1_values, y2_values, y3_values, y4_values, y5_values, vars, costos

x_values, y1_values, y2_values, y3_values, y4_values, y5_values, vars, costos = cargar_datos()


layout = dbc.Container([
    dcc.Location(id='url', refresh=False),  # Componente para detectar cambios en la URL
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),  # Intervalo para actualizar los datos
    html.Br(),
    dbc.Row([dbc.Col(
        html.H4('Cantidad de trabajadores por mes', style={'text-align': 'center'})
    ),
        dbc.Col(
            html.H4('Nómina mensual de trabajadores', style={'text-align': 'center'})
        )]),
    dbc.Row([
        dbc.Col(
            dbc.Tabs(
                [
                    dbc.Tab(dcc.Graph(id='graph1'),
                    label="Gráfica", tab_id="grafica-1"),
                    dbc.Tab(html.Div(id = 'res-1'),label="Información", tab_id="info-1"),
                ],
                id="card-trabajadores",
                active_tab="grafica-1",
            ), width=6
        ),
        dbc.Col(
            dbc.Tabs(
                [
                    dbc.Tab(dcc.Graph(id='graph2'),
                    label="Gráfica", tab_id="grafica-2"),
                    dbc.Tab(html.Div(id = 'res-2'),label="Información", tab_id="info-2"),
                ],
                id="card-nomina",
                active_tab="grafica-2",
            ), width=6
        )
    ]),
    dbc.Row(id = 'cards', className='mt-4'), html.Div(
    html.H6('Valentina Cabrera y Valentina Bustamante', className = 'badge bg-dark', style={'font-size':'12px'}), 
    style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'justifyContent': 'center'})
    
    ], fluid=True)

@dash.callback(
    [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('res-1','children'), Output('res-2','children')],
    [Input('url', 'pathname'), Input('interval-component', 'n_intervals')]
)
def update_graphs(pathname, n):
    # Recargar datos
    x_values, y1_values, y2_values, y3_values, y4_values, y5_values, vars, costos = cargar_datos()
    
    fig1 = {
        'data': [
            go.Scatter(
                x=x_values,
                y=y1_values,
                mode='lines',
                name='Experimentados',
                line={'color': '#ffc107'}
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

    fig2 = {
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
    res1 = []
    for i in range(len(x_values)):
        res1.append(html.H5(f'{x_values[i].capitalize()}:',className = 'badge bg-light'))
        res1.append(html.H6(f'En el mes de {x_values[i]}, deberían haber {int(y1_values[i])} trabajadores experimentados y {int(y2_values[i])} en entrenamiento.', style={'font-size':'15px', 'padding-left':'12px'}))

    res2 = []
    for i in range(len(x_values)):
        res2.append(html.H5(f'{x_values[i].capitalize()}:',className = 'badge bg-light'))
        res2.append(html.H6(f'En el mes de {x_values[i]}, se pagarían ${int(y3_values[i])} en total, con ${int(y4_values[i])} en trabajadores experimentados y ${int(y5_values[i])} en entrenamiento.', style={'font-size':'15px', 'padding-left':'12px'}))
    
    return fig1, fig2, res1, res2


@dash.callback(
    Output('cards','children'),
    Input('url', 'pathname'), Input('interval-component', 'n_intervals')
)

def actualizar_card(pathname, n):
    x_values, y1_values, y2_values, y3_values, y4_values, y5_values, vars, costos = cargar_datos()

    cards = [
        dbc.Col(
            html.Div([
                html.H6('Trabajadores finales', className='card-header', style={'text-align': 'center', 'height': '4rem'}),
                html.H4(f'{int(vars[int(len(vars)/2) - 1] + vars[-1])}', className='card-body'),
            ], className='card text-white bg-dark mb-3', style={'text-align': 'center', 'width': '12rem', 'height': '7rem'}), align='center'
        ),
        dbc.Col(
            html.Div([
                html.H6('Total de trabajadores', className='card-header', style={'text-align': 'center', 'height': '4rem'}),
                html.H4(f'{int(vars[1] + sum(vars[int(len(vars)/2):]))}', className='card-body')
            ], className='card text-white bg-dark mb-3', style={'text-align': 'center', 'width': '12rem', 'height': '7rem'}), align='center'
        ),
        dbc.Col(
            html.Div([
                html.H6(['Costo', html.Br(), 'total'], className='card-header', style={'text-align': 'center', 'height': '4rem'}),
                html.H4(f'${int(sum(y3_values))}', className='card-body')
            ], className='card border-dark mb-3', style={'text-align': 'center', 'width': '12rem', 'height': '7rem'}), align='center'
        ),
        dbc.Col(
            html.Div([
                html.H6('Costo experimentados', className='card-header', style={'text-align': 'center', 'height': '4rem'}),
                html.H4(f'${int(sum(y1_values) * costos[0])}', className='card-body')
            ], className='card border-dark mb-3', style={'text-align': 'center', 'width': '12rem', 'height': '7rem'}), align='center'
        ),
        dbc.Col(
            html.Div([
                html.H6('Costo entrenamiento', className='card-header', style={'text-align': 'center', 'height': '4rem'}),
                html.H4(f'${int(sum(y2_values) * costos[1])}', className='card-body')
            ], className='card border-dark mb-3', style={'text-align': 'center', 'width': '12rem', 'height': '7rem'}), align='center'
        )
    ]

    return cards
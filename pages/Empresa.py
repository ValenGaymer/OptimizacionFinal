import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__)

layout = html.Div([
    html.H2('V2 Solutions: ¡Tu aliado en la optimización!'),
    html.P("V2 Solutions es una empresa nacida en Barranquilla en el año 2024. Nuestro propósito es ayudar a las empresas a optimizar todos los procesos que necesiten de la mano con los integrantes de nuestra compañía."),
    html.P("")
])
    
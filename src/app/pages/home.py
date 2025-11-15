import dash
from dash import Dash, html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
dash.register_page(__name__, path='/')

layout =  dbc.Container([
    html.H1("Welcome to ML2025 August Session!"),
    html.H1("Fun Learning in ML!!!"),

], fluid=True)
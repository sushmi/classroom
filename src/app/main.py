# Import packages
from dash import Dash, html, Output, Input, dcc
import dash_bootstrap_components as dbc

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
from pages.home import *

# Navigation Bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Assignment 1: Predicting Car Price", href="/model1")),
    ],
    brand="ML2025 August Coursework!",
    brand_href="/",
    color="primary",
    dark=True,
)


app.layout = html.Div([
    navbar,
    dash.page_container
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
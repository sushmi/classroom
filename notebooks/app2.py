# Import packages
from dash import Dash, html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import pickle
import dill
from LinearRegression import NormalRegression

#from my_model_module import Normal_Regression  
# Initialize the app with a theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# paths of all components for car price predictions

# load all components
scaler_new = pickle.load(open('./models/a2-minmax-scalar.model', 'rb'))
# ===== Load Model =====
old_model = pickle.load(open('./models/cars_a1.model', 'rb'))
new_model = dill.load(open('./models/car-a2-1-prediction.model', 'rb'))                        

# Numeric columns
num_cols = ['max_power', 'engine', 'year']
num_cols1 = ['max_power', 'engine', 'mileage']

# Categories for dropdowns

# Layout
app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H1(" Car Price Prediction", className="text-center mb-4"),
                    html.Hr(),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Engine (cc)"),
                            dcc.Input(id="engine", type="number", value=1200, style={"width": "100%"})
                        ], width=6),

                        dbc.Col([
                            dbc.Label("Max Power (bhp)"),
                            dcc.Input(id="max_power", type="number", value=80, style={"width": "100%"})
                        ], width=6),
                        
                        dbc.Col([
                            dbc.Label("Mileage (km/l)"),
                            dcc.Input(id="mileage", type="number", value=15, style={"width": "100%"})
                        ], width=6),
                    ], className="mb-3"),

                    dbc.Button("Predict Price", id="submit", color="primary", className="w-100 mb-3"),
                    html.Div(id="prediction_result", className="text-center fs-4 fw-bold")
                ]),
                className="shadow p-4"
            ),
            width=8,
            className="mx-auto my-5"
        )
    ),
    fluid=True
)

#df[['max_power', 'engine', 'mileage']]
# Prediction callback
@callback(
    Output("prediction_result", "children"),
    Input("submit", "n_clicks"),
    State("max_power", "value"),
    State("engine", "value"),
    State("mileage", "value"),
    prevent_initial_call=True
)
def predict_price(n, max_power,  engine,  mileage):
    # Create dataframe for input
    X = pd.DataFrame([{
        "max_power": max_power,
        "engine": engine,
        "mileage": mileage
    }])

    # Scale numeric features
    X[num_cols1] = scaler_new.transform(X[num_cols1])
    
    X.insert(0,'intercept',1)
    # Predict
    price = np.round(np.exp(new_model.predict(X)), 2)[0]

    return f" Predicted Price: {price}"


# Run app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8051)

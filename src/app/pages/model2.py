import dash
from dash import Dash, html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
dash.register_page(__name__, path='/model2', name='Assignment 2: Predicting Car Price', title='Assignment 2: Predicting Car Price')

# Explain Text
text = html.Div([
    html.H1("The second Assignment Predict Car Prices"),
])

# ['year', 'seller_type', 'transmission', 'engine', 'max_power']
x1_year = html.Div(
    [
        dbc.Label("Year (x1)", html_for="example-email"),
        dbc.Input(id="year", type="number"),
        dbc.FormText(
            "This is the value for year",
            color="secondary",
        ),
    ],
    className="assignment-2",
)

# Manual       7078
# Automatic    1050
x2_transmission = html.Div(
    [
        dbc.Label("Transmission (x2)", html_for="example-email"),
        dbc.Input(id="transmission", type="text"),
        dbc.FormText(
            "This is the value for transmission : 'Manual', 'Automatic'",
            color="secondary",
        ),
    ],
    className="assignment-2",
)

x3_km_driven = html.Div(
    [
        dbc.Label("km_driven (x3)", html_for="example-email"),
        dbc.Input(id="km_driven", type="number"),
        dbc.FormText(
            "This is the value for km driven",
            color="secondary",
        ),
    ],
    className="assignment-2",
)


x4_max_power = html.Div(
    [
        dbc.Label("Max Power (x4)", html_for="example-email"),
        dbc.Input(id="max_power", type="number"),
        dbc.FormText(
            "This is the value for max power",
            color="secondary",
        ),
    ],
    className="assignment-2",
)

x5_mileage = html.Div(
    [
        dbc.Label("Mileage (x5)", html_for="example-email"),
        dbc.Input(id="mileage", type="number"),
        dbc.FormText(
            "This is the value for mileage",
            color="secondary",
        ),
    ],
    className="assignment-2",
)

submit_model = html.Div([
            dbc.Button(id="submit_model", children="Predict Car Price", color="primary", className="me-1"),
            dbc.Label("Car price (y) is: "),
            html.Output(id="y_model2", children="")
], style={'marginTop':'10px'})

#['year', 'transmission', 'km_driven', 'max_power', 'mileage']
form =  dbc.Form([
    x1_year,
    x2_transmission,
    x3_km_driven,
    x4_max_power,
    x5_mileage,
    submit_model
],
className="model-2")


# Dataset Example
from dash import Dash, dash_table
import pandas as pd


layout =  dbc.Container([
        form,
    ], fluid=True)


@callback(
    Output(component_id="y_model2", component_property="children"),
    State(component_id="year", component_property="value"),
    State(component_id="transmission", component_property="value"),
    State(component_id="km_driven", component_property="value"),
    State(component_id="max_power", component_property="value"),
    State(component_id="mileage", component_property="value"),
    Input(component_id="submit_model", component_property='n_clicks'),
    prevent_initial_call=True
)
def calculate_car_price_model_submit(x1_year, x2_transmission, x3_km_driven, x4_max_power, x5_mileage, submit):
    pred = calculate_car_price_model2(x1_year, x2_transmission, x3_km_driven, x4_max_power, x5_mileage)
    return f"{pred}"

# def get_coeff():
#     from utils import load
#     model = load('./models/myModel.pickle')
#     return model.coef_

# def calculate_model(x_1,x_2):
#     from utils import load
#     import pandas as pd
#     import numpy as np
#     model = load('./models/myModel.pickle')
#     X = np.array([x_1,x_2]).reshape(-1,2)
#     X = pd.DataFrame(X, columns=['x1', 'x2']) 
#     pred = model.predict(X)
#     return pred


def calculate_car_price_model2(x1_year, x2_transmission, x3_km_driven, x4_max_power, x5_mileage):
    from utils import load
    import pandas as pd
    import numpy as np
    from datetime import date
    import numpy as np

    print(f"year={x1_year} transmission={x2_transmission} km_driven={x3_km_driven} max_power={x4_max_power} mileage={x5_mileage}")

    model = load('./models/a2/linear_regression_model.pkl')
    scalar_km_driven = load('./models/a2/standard_scaler_km_driven.pkl')
    scalar_mileage = load('./models/a2/standard_scaler_mileage.pkl')
    scalar_max_power = load('./models/a2/standard_scaler_max_power.pkl')
    scalar_year = load('./models/a2/standard_scaler_year.pkl')

    age = date.today().year - int(x1_year)
    year = scalar_year.transform([age])

    km_driven1p = np.log1p(x3_km_driven)
    km_driven = scalar_km_driven.transform([km_driven1p])

    max_power1p = np.log1p(x4_max_power)
    max_power = scalar_max_power.transform([max_power1p])

    mileage = scalar_mileage.transform([x5_mileage])


    X = np.array([year[0], x2_transmission, km_driven[0], max_power[0], mileage[0]]).reshape(-1,5)
    X = pd.DataFrame(X, columns = ['year', 'transmission', 'km_driven', 'max_power', 'mileage']) 
    pred = model.predict(X)
    price = np.exp(pred[0]) .round(2).item()

    return f"THB {price:,.2f}"
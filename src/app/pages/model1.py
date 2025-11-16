import dash
from dash import Dash, html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
dash.register_page(__name__, path='/model1')

# Explain Text
text = html.Div([
    html.H1("The first Assigment Preidct Car Prices"),
])

# ['year', 'seller_type', 'transmission', 'engine', 'max_power']
year = html.Div(
    [
        dbc.Label("Year (x1)", html_for="example-email"),
        dbc.Input(id="year", type="number"),
        dbc.FormText(
            "This is the value for year",
            color="secondary",
        ),
    ],
    className="assignment-1",
)

seller_type = html.Div(
    [
        dbc.Label("Seller Type (x2)", html_for="example-email"),
        dbc.Input(id="seller_type", type="text"),
        dbc.FormText(
            "This is the value for seller type : 'Individual', 'Dealer', 'Trustmark Dealer'",
            color="secondary",
        ),
    ],
    className="assignment-1",
)

# Manual       7078
# Automatic    1050
transmission = html.Div(
    [
        dbc.Label("Transmission (x3)", html_for="example-email"),
        dbc.Input(id="transmission", type="text"),
        dbc.FormText(
            "This is the value for transmission : 'Manual', 'Automatic'",
            color="secondary",
        ),
    ],
    className="assignment-1",
)

engine = html.Div(
    [
        dbc.Label("Engine (x4)", html_for="example-email"),
        dbc.Input(id="engine", type="text"),
        dbc.FormText(
            "This is the value for engine",
            color="secondary",
        ),
    ],
    className="assignment-1",
)

max_power = html.Div(
    [
        dbc.Label("Max Power (x5)", html_for="example-email"),
        dbc.Input(id="max_power", type="text"),
        dbc.FormText(
            "This is the value for max power",
            color="secondary",
        ),
    ],
    className="assignment-1",
)

# Creating FORM
# x_1 = html.Div(
#     [
#         dbc.Label("x_1", html_for="example-email"),
#         dbc.Input(id="x_1", type="number", placeholder="Put a value for x_1"),
#         dbc.FormText(
#             "This is the value for x_1",
#             color="secondary",
#         ),
#     ],
#     className="mb-3",
# )

# x_2 = html.Div(
#     [
#         dbc.Label("x_2", html_for="example-email"),
#         dbc.Input(id="x_2", type="number", placeholder="Put a value for x_2"),
#         dbc.FormText(
#             "This is the value for x_2",
#             color="secondary",
#         ),
#     ],
#     className="mb-3",
# )

# submit_hardcode = html.Div([
#             dbc.Button(id="submit_hardcode", children="calculate y using hardcode", color="primary", className="me-1"),
#             dbc.Label("y is: "),
#             html.Output(id="y_hardcode", children="")
# ], style={'marginTop':'10px'})

submit_model = html.Div([
            dbc.Button(id="submit_model", children="Predict Car Price", color="primary", className="me-1"),
            dbc.Label("Car price (y) is: "),
            html.Output(id="y_model", children="")
], style={'marginTop':'10px'})

# ['year', 'seller_type', 'transmission', 'engine', 'max_power']
form =  dbc.Form([
    year,
    seller_type,
    transmission,
    engine,
    max_power,
    submit_model
],
className="mb-3")


# Dataset Example
from dash import Dash, dash_table
import pandas as pd


layout =  dbc.Container([
        form,
    ], fluid=True)

# @callback(
#     Output(component_id="y_hardcode", component_property="children"),
#     State(component_id="x_1", component_property="value"),
#     State(component_id="x_2", component_property="value"),
#     Input(component_id="submit_hardcode", component_property='n_clicks'),
#     prevent_initial_call=True
# )
# def calculate_y_hardcode(x_1, x_2, submit):
#     print(x_1)
#     print(x_2)
#     print(submit)
#     return x_1 + x_2

# @callback(
#     Output(component_id="y_model_", component_property="children"),
#     State(component_id="x_1", component_property="value"),
#     State(component_id="x_2", component_property="value"),
#     Input(component_id="submit_model", component_property='n_clicks'),
#     prevent_initial_call=True
# )
# def calculate_y_model(x_1, x_2, submit):
#     pred = calculate_model(x_1,x_2)
#     coef = get_coeff()
#     return f" model said: {pred=} {coef_=}"


@callback(
    Output(component_id="y_model", component_property="children"),
    State(component_id="year", component_property="value"),
    State(component_id="seller_type", component_property="value"),
    State(component_id="transmission", component_property="value"),
    State(component_id="engine", component_property="value"),
    State(component_id="max_power", component_property="value"),
    Input(component_id="submit_model", component_property='n_clicks'),
    prevent_initial_call=True
)
def calculate_car_price_model_submit(year, seller_type, transmission, engine, max_power, submit):
    pred = calculate_car_price_model(year, seller_type, transmission, engine, max_power)
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


def calculate_car_price_model(year, seller_type, transmission, engine, max_power):
    from utils import load
    import pandas as pd
    import numpy as np
    model = load('./models/a1_predict_car_price.model')
    seller_type_encoder = load('./models/a1_encoder_seller_type.model')
    transmission_encoder = load('./models/a1_encoder_transmission.model')

    encoded_seller_type = seller_type_encoder.transform([seller_type])
    print(f"{seller_type} encoded_seller_type: {encoded_seller_type}")

    encoded_transmission = transmission_encoder.transform([transmission])
    print(f"{transmission} encoded_transmission: {encoded_transmission}")

    X = np.array([year, encoded_seller_type[0], encoded_transmission[0], engine, max_power]).reshape(-1,5)
    X = pd.DataFrame(X, columns=['year', 'seller_type', 'transmission', 'engine', 'max_power']) 
    pred = model.predict(X)
    price = np.exp(pred[0]) .round(2).item()
    return f"{price:.2f}"
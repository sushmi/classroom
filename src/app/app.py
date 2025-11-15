from dash import Dash, html

# Initialize the app
# Don't forget to install the required Dash version (2.17.0 or later)
# uv add dash 

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [html.Div(children='Hello World')]

if __name__ == '__main__':
    app.run(debug=True)

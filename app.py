import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from maindash import app
from pages.single import make_single_layout

server = app.server
app.layout = make_single_layout()

if __name__ == "__main__":
    app.run_server(debug=True)

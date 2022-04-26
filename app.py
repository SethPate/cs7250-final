import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from maindash import app
from pages.main import main_layout

server = app.server
app.layout = main_layout

if __name__ == "__main__":
    app.run_server(debug=True)

import dash
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from maindash import app
from utils.functions import matrix_fig
from utils.functions import update_fig


def get_layout(params):
    layout = html.Div(
        [
            html.H1("Nonlinearity", id="nln-section"),
            html.Div(),
            html.Hr(),
            dcc.Markdown(
                """
        ## purpose of a feedforward layer

        """
            ),
            html.Div(dcc.Graph(id="linear")),
            dcc.Markdown(
                """
        ## residual connections
        - show two layers normally
        - show three layers residually
        """
            ),
            html.Div(dcc.Graph(id="relu")),
            dcc.Markdown(
                """
        ## layer norm

        Transform the outputs of a certain layer to mean 0 and std 1.
        Layer normalization is an alternative to batch normalization.

        """
            ),
            html.Div(dcc.Graph(id="norm")),
        ]
    )
    return layout


@app.callback(Output("linear", "figure"), Input("datastore", "data"))
def update_linear(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return update_fig(params, "linear", "linear")


@app.callback(Output("relu", "figure"), Input("datastore", "data"))
def update_relu(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return update_fig(params, "relu", "ReLU")


@app.callback(Output("norm", "figure"), Input("datastore", "data"))
def update_norm(params):
    if not params:
        return
    elif params["update_figs"] is False:
        raise dash.exceptions.PreventUpdate
    else:
        return update_fig(params, "norm", "normalized")

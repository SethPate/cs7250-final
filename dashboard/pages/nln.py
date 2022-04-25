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
        ## linear transformations

        Immediately after the attention block comes a linear transformation, in which
        we multiply the **attention output** by some number, and then add another number
        (a **bias**) to it. Here is what our encoded sample looks like afterward:

        """
            ),
            html.Div(dcc.Graph(id="linear")),
            dcc.Markdown(
                """
        ## rectified linear unit (ReLU)

        The ReLU is a simple function. When you give it a matrix, it
        just changes all the negative numbers to 0. This is a **nonlinear
        transformation**, and using such a nonlinearity as an **activation function**
        is a key part of deep learning.
        Nonlinear functions can learn more complex patterns than linear functions.

        Here you can see the impact of the ReLU on our linear output. Quite a change!
        """
            ),
            html.Div(dcc.Graph(id="relu")),
            dcc.Markdown(
                """
        ## layer normalization

        Every time we go through one of these nonlinear transformations, our data
        get a little less normally distributed. We'd like them to be clustered around 0,
        though. **Layer normalization** is a commonly used technique that scales the outputs
        of the layer by subtracting their mean dividing them by their standard deviation.
        This seems to help the model train more quickly, more *stably*.

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

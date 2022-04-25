from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app
from utils.functions import matrix_fig
from utils.functions import update_fig


def get_layout():
    return html.Div(
        [
            html.H1("Decoder", id="decoder-section"),
            html.Hr(),
            dcc.Markdown(
                """
            Now that we have encoded the information from the sample,
            we have to **decode** it to answer our original question:
            was this a positive or negative movie review?

            In this simple 'binary classification' task, we only need a linear
            transformation to determine a single number. That number
            represents the model's confidence that the sample is positive.

            - show layer * weight = guess

            Transformer models with more complicated tasks, like language modeling,
            have more complicated decoders. Translation network. Decoder-only.
        """
            ),
            html.Div(id="decoder"),
            dcc.Markdown(
                """
            logistic pass
            """
            ),
            html.Div(id="final"),
            dcc.Markdown(
                """
            closing copy
            """
            ),
        ]
    )


@app.callback(Output("decoder", "children"), Input("datastore", "data"))
def update_decoder(params):
    if not params:
        return
    else:
        return update_fig(params, "decoder", "decoder")


@app.callback(Output("final", "children"), Input("datastore", "data"))
def update_final(params):
    if not params:
        return
    else:
        return update_fig(params, "final", "final")

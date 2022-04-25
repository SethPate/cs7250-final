from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app

explain = dcc.Markdown(
    """
    Transformers are cool and they are used in a lot of places.

    They can do this and that. Here are some famous transformers.

    They have cool results in log-linear charts.

    Here is what we are going to do -- we are going to classify movie
    reviews.

    This is the sample we have right now. You can change it if you want,
    and the rest of this page will update to show the new data.
"""
)


def make_dropdown(params):
    ix = params["current_sample_ix"]
    samples = [0, 1]
    sample_ids = [f"Sample {i+1}" for i in samples]
    return html.Div(
        [
            dcc.Dropdown(sample_ids, sample_ids[0], id="dropdown-samples"),
        ],
    )


def make_layout(params):
    ix = params["current_sample_ix"]
    sample = params["layerdata"][ix]["sample"]
    dropdown = make_dropdown(params)
    return html.Div(
        [
            explain,
            dropdown,
            html.P(" ".join(sample)),
        ],
        id="home",
    )

import numpy as np
import pandas as pd
import plotly.express as px
from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

from .style import stylesheet
from . import data


def calc_div_height(words):
    return len(words) * 20 + 60 + 20


params = {
    "x_space_between_nodes": 200,
    "y_space_between_nodes": 20,
    "x_first_node": 100,
    "y_first_node": 60,
}

words = [
    "My",
    "name",
    "is",
    "TESTROBOT"
]

div_height = calc_div_height(words)

layout_cytoscape = data.get_cyto_layout(words, params)

selecty_outputy = html.P(id='selecty-outputy',children='WHAZUP')

# TODO: use translate trick to position by cneter point https://stackoverflow.com/questions/15328416/position-by-center-point-rather-than-top-left-point

buttons_samples = html.Div(
    [
        html.Button(
            "<",
            id=f"button-sample-back",
        ),
        html.Span(f"Sample {'1'.zfill(3)}", id=f"text-id-sample"),
        html.Button(
            ">",
            id=f"button-sample-forward",
        ),
    ],
    style={"position": "relative", "left": f"40px", "display": "inline-block"},
)


buttons_heads = html.Div(
    [
        html.Button(
            "<",
            id=f"button-head-back",
        ),
        html.Span(f"Head {'1'.zfill(2)}", id=f"text-id-head"),
        html.Button(
            ">",
            id=f"button-head-forward",
        ),
    ],
    style={"position": "relative", "display": "inline-block", "left": f"125px"},
)

layout = html.Div(
    [html.H1("Explorer view"), 
    layout_cytoscape, 
    selecty_outputy,
    buttons_samples, 
    buttons_heads]
)

@app.callback(Output('selecty-outputy', 'children'),
                Input('explorer-view', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        return "OH YEAH"

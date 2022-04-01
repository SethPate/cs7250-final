import dash_cytoscape as cyto
import numpy as np
import pandas as pd
import plotly.express as px
from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

from . import data
from .style import stylesheet


def calc_div_height(words):
    return len(words) * 20 + 60 + 20


params = {
    "x_space_between_nodes": 200,
    "y_space_between_nodes": 20,
    "x_first_node": 100,
    "y_first_node": 60,
}

dict_sentences = data.get_sentences()
words = [
    "My",
    "name",
    "is",
    "Pedro",
    "and",
    "I",
    "am",
    "a",
    "student",
]

div_height = calc_div_height(words)


# TODO: separate logic for generating nodes and edges into several functions
# TODO: move data logic into a separate python file ("model")
# TODO: add buttons below  graph to change sample, head
# TODO: add tooltips to nodes
# TODO: add avg and probabilities below output and class columns
# TODO: when highlighting at least one node, remove all attention edges unrelated to the selected nodes
# TODO: enable using real attention data for edges
# TODO: generate a good line width map for edges
# TODO: generate a good color map for the outputs and the class


elements = data.get_node_dicts(words, params) + data.get_node_headers(params)

# TODO: consider having several views for viewing several layers or heads of attention (?)

layout_cytoscape = cyto.Cytoscape(
    id="explorer-view",
    layout={"name": "preset", "fit": True},
    style={"width": "100%", "height": f"{div_height}px"},
    panningEnabled=False,
    zoomingEnabled=False,
    elements=elements,
    stylesheet=stylesheet,
    autoungrabify=True,
    autounselectify=False,
)

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
    style={"position": "relative", "left": f"40px", "display":"inline-block"},
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
    style={"position": "relative", "display":"inline-block", "left": f"125px"},
)

layout = html.Div(
    [html.H1("Explorer view"), layout_cytoscape, buttons_samples, buttons_heads]
)

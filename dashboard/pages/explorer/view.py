import numpy as np
import pandas as pd
import plotly.express as px
from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

from . import data

params = {
    "x_space_between_nodes": 200,
    "y_space_between_nodes": 20,
    "x_first_node": 50,
    "current_top_node_word": 0,
    "current_top_node_attention": 0,
    "y_first_node": 9,
    "max_nodes_to_visualize": 15,
    "current_sample": 0,
    "current_head": 0,
    "n_weights_ff": 128,
    "y_first_node_ff": 5,
    "x_space_between_nodes_ff": 10,
    "y_space_between_nodes_ff": 9,
    "n_heads": 4,
}

params.update(data.get_dummy_sentences(params))

# TODO: separate logic for generating nodes and edges into several functions
# TODO: add buttons below  graph to change  head
# TODO: add tooltips to nodes
# TODO: add avg and probabilities below output and class columns
# TODO: when highlighting at least one node, remove all attention edges unrelated to the selected nodes
# TODO: enable using real attention data for edges
# TODO: generate a good line width map for edges
# TODO: generate a good color map for the class
# TODO: consider having several views for viewing several layers
# or heads of attention (?)

layout_cytoscape = data.get_cyto_layout(params)


# TODO: use translate trick to position by cneter point https://stackoverflow.com/questions/15328416/position-by-center-point-rather-than-top-left-point


scroll_btn_x_positions = [42, 219]

current_sentence = html.Div(
    [
        html.Span("Sentence: ", style={"font-weight": "bold"}),
        html.Span(
            "",
            id="text-sentence",
        ),
        html.Br(),
        html.Br(),
    ],
    className="text-sentence",
    style={
        "left": "27px",
    },
)

headers = html.Div(
    [
        html.P(
            "Words",
            className="header-text",
            style={
                "left": "27px",
            },
        ),
        html.P(
            "Attention",
            className="header-text",
            style={
                "left": "170px",
            },
        ),
        html.P(
            "Fully-connected weights",
            className="header-text",
            style={
                "left": "227px",
            },
        ),
        html.P(
            "Class",
            className="header-text",
            style={
                "left": "323px",
            },
        ),
    ]
)

buttons_up = html.Div(
    [
        html.Button(
            "↑",
            id="button-word-up",
            className="button-scroll",
            style={
                "position": "relative",
                "display": "inline-block",
                "left": f"{scroll_btn_x_positions[0]}px",
            },
        ),
        html.Button(
            "↑",
            id="button-attention-up",
            className="button-scroll",
            style={
                "position": "relative",
                "display": "inline-block",
                "left": f"{scroll_btn_x_positions[1]}px",
            },
        ),
    ]
)

buttons_down = html.Div(
    [
        html.Button(
            "↓",
            id="button-word-down",
            className="button-scroll",
            style={
                "position": "relative",
                "display": "inline-block",
                "left": f"{scroll_btn_x_positions[0]}px",
            },
        ),
        html.Button(
            "↓",
            id="button-attention-down",
            className="button-scroll",
            style={
                "position": "relative",
                "display": "inline-block",
                "left": f"{scroll_btn_x_positions[1]}px",
            },
        ),
    ]
)


buttons_samples = html.Div(
    [
        html.Button(
            "<",
            id="button-sample-back",
        ),
        html.Span(f"Sample {'1'.zfill(3)}", id="text-id-sample"),
        html.Button(
            ">",
            id="button-sample-forward",
        ),
    ],
    style={"position": "relative", "left": "-10px", "display": "inline-block"},
)


buttons_heads = html.Div(
    [
        html.Button(
            "<",
            id="button-head-back",
        ),
        html.Span(f"Head {'1'.zfill(2)}", id=f"text-id-head"),
        html.Button(
            ">",
            id="button-head-forward",
        ),
    ],
    style={"position": "relative", "display": "inline-block", "left": f"72px"},
)

layout = html.Div(
    [
        dcc.Store(id="explorer-view-store", data=params),
        html.H1("Explorer view"),
        current_sentence,
        headers,
        buttons_up,
        layout_cytoscape,
        buttons_down,
        buttons_samples,
        buttons_heads,
    ]
)

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from maindash import app

from .style import stylesheet  # specific to cytoscape

WORDS_PER_ROW = 7  # at 800px width


def get_elements(params):
    """Makes nodes for the cytoscape."""

    element_list = []

    sample_ix = params["current_sample_ix"]
    words = params["layerdata"][sample_ix]["sample"]
    wordmap = get_wordmap(words)
    element_list += wordmap

    return element_list


def get_spans(params):
    """
    Displayed below the cytoscape. Shows attention by modifying
    word opacity according to the attention value, relative to the selected word.
    """

    sample_ix = params["current_sample_ix"]
    selected_word_ix = params["selected_word_ix"]
    words = params["layerdata"][sample_ix]["sample"]
    attn_weights = params["layerdata"][sample_ix]["attention"]

    if selected_word_ix is None:  # need not be selected
        attn = np.ones(len(words))
    else:
        attn = [
            attn_weights[selected_word_ix][i] if i != selected_word_ix else 1.0
            for i in range(len(words))
        ]

    # set minimum opacity
    opacity = np.array(attn)
    opacity[opacity < 0.2] = 0.2

    spans = []
    tooltips = []
    for i, w in enumerate(words):
        display = w + " "
        o = opacity[i]
        _id = f"span_{i}"
        span = html.Span(display, id=_id, className="attn-text", style={"opacity": o})
        spans.append(span)
        tooltip = dbc.Tooltip(f"attn value: {round(o,2)}", target=_id)
        tooltips.append(tooltip)

    # tooltips to show attn value on hover
    return spans, tooltips


def get_wordmap(words):
    """
    Nodes for the cytoscape. 'ix' refers to the word order in the sentence.
    """

    elements = []
    for i, w in enumerate(words):
        word_node = {
            "data": {"id": f"word_{i}", "ix": i, "label": w},
            "classes": "node-word",
        }
        elements.append(word_node)
    return elements


def get_cyto_layout(params, n_rows):
    elements = get_elements(params)

    layout_cytoscape = cyto.Cytoscape(
        id="attn-cyto",
        layout={
            "name": "grid",
            "fit": True,
            "cols": WORDS_PER_ROW,
            "avoidOverlapPadding": 5,
            "condense": True,
        },
        style={
            "width": "800px",
            "height": f"{n_rows * 30}px",
        },
        panningEnabled=False,
        zoomingEnabled=False,
        elements=elements,
        stylesheet=stylesheet,
        autoungrabify=True,
        autounselectify=False,
    )

    return layout_cytoscape


explain = dcc.Markdown(
    """
    ## query, key, value attention

    - show q, k, v, matrices with their words
    - show q*k = qk
    - show scaled qk
    - show softmax(scaled qk)
    - show softmax * v = output

    ## multi head attention

    And also a bit on how this works.
    """
)


def get_layout(params):
    """
    Construct the whole attention module, including the cytoscape element
    at the center.
    """

    description = html.P(
        "Mouse over words to see their attention value below. Click to select."
    )

    current_sample_ix = params["current_sample_ix"]
    words = params["layerdata"][current_sample_ix]["sample"]

    paragraph = html.P(" ".join(words))

    rows = len(words) // WORDS_PER_ROW
    cyto_layout = get_cyto_layout(params, n_rows=rows)

    spans, tooltips = get_spans(params)
    spans += tooltips  # roll tolltips into layout

    layout = html.Div(
        [
            dcc.Store(id="datastore", data=params),
            html.H1("Attention"),
            html.Hr(),
            description,
            html.Hr(),
            paragraph,
            cyto_layout,
            html.P(id="span-holder", children=spans),
            html.P(id="display", children=params["selected_word_ix"]),
            html.Hr(),
            explain,
        ]
    )

    return layout


@app.callback(Output("span-holder", "children"), Input("datastore", "data"))
def span_update(data):
    if not data:
        return
    else:
        spans, tooltips = get_spans(data)
        return spans + tooltips

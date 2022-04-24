import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input,Output,State
from pages.maindash import app
import numpy as np
import numpy as np
import pandas as pd
from scipy.special import softmax
import pickle

from .style import stylesheet

WORDS_PER_ROW = 7 # at 800px width
fake_data_path = "./data/fake_data.pickl"


def get_dummy_data(params):
    """
    Called by view.py to supplement params.
    """
    sample_ix = params['current_sample_ix']

    with open(fake_data_path, 'rb') as f:
        fake_data = pickle.load(f)

    sample_data = fake_data[sample_ix]

    return sample_data 

def get_elements(params):
    element_list = []

    sample = params['sample'] # list of tokens
    wordmap = get_wordmap(sample)
    element_list += wordmap 

    return element_list

def get_spans(params):
    selected_word_ix = params['selected_word_ix']
    words = params['sample']
    attn_weights = params['attention']

    if not selected_word_ix: # need not be selected
        attn = np.ones(len(words))
    else:
        attn = [attn_weights[selected_word_ix][i] \
            if i != selected_word_ix else 1. \
            for i in range(len(words))]

    # set minimum opacity
    opacity = np.array(attn)
    opacity[opacity < .2] = .2

    spans = []
    tooltips = []
    for i,w in enumerate(words):
        display = w + " "
        o = opacity[i]
        _id = f"span_{i}"
        span = html.Span(display, id=_id, className='attn-text', style={'opacity':o})
        spans.append(span)
        tooltip = dbc.Tooltip(f"attn value: {round(o,2)}", target=_id)
        tooltips.append(tooltip)

    # tooltips to show attn value on hover
    return spans, tooltips

def get_wordmap(words):
    elements = []
    for i, w in enumerate(words):
        word_node = {
            "data": {"id": f"word_{i}", "ix": i, "label": w},
            "classes": "node-word"
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
            "cols":WORDS_PER_ROW,
            "avoidOverlapPadding":5,
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


# Test case to show the selection reactively
@app.callback(
    Output("display","children"),
    Input("explorer-view-store","data"))
def displayer(data):
    return data['selected_word_ix']

"""
When the data changes, regenerate the spans and their tooltips.
"""
@app.callback(
    Output("span-holder","children"),
    Input("explorer-view-store","data"))
def span_update(params):
    if not params:
        return
    new_spans, new_tooltips = get_spans(params)
    return new_spans + new_tooltips

"""
Update the data to reflect a selected word from the cytoscape.
"""
@app.callback(
    Output("explorer-view-store", "data"),
    Input("attn-cyto", "selectedNodeData"),
    State("explorer-view-store", "data"))
def selectHelper(selection_list, data):
    if not selection_list:
        data['selected_word_ix'] = None
    else:
        data['selected_word_ix'] = selection_list[0]['ix']
    return data

def get_layout():
    params = {
        "current_sample_ix": 0,
        "selected_word_ix": 0,
        "current_head": 0,
        "n_heads": 4
    }

    description = html.P("The world of attention sure is interesting.")

    params.update(get_dummy_data(params))

    current_sample_ix = params['current_sample_ix']
    words = params['sample']

    paragraph = html.P(" ".join(words))
    
    rows = len(words) // WORDS_PER_ROW
    cyto_layout = get_cyto_layout(params, n_rows=rows)

    spans, tooltips = get_spans(params)
    spans += tooltips # roll tolltips into layout

    layout = html.Div(
        [
            dcc.Store(id="explorer-view-store", data=params),
            html.H1("Attention"),
            html.Hr(),
            description,
            html.Hr(),
            paragraph,
            cyto_layout,
            html.P(id="span-holder",children=spans),
            html.P(id="display",children=params['selected_word_ix'])
        ]
    )

    return layout

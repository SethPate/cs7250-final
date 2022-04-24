import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input,Output
from app import app
import numpy as np
import numpy as np
import pandas as pd
from scipy.special import softmax

from .style import stylesheet

WORDS_PER_ROW = 7 # at 800px width


def get_dummy_data(params):
    """
    Called by view.py to supplement params.
    """
    raw_sentences = [
        "I went and saw this movie last night after being coaxed to by a few friends of mine. I'll admit that I was reluctant to see it because from what I knew of Ashton Kutcher he was only able to do comedy.",
        "I think this is one of those few movies that I want to rate it as low as possible just to pay it a compliment.",
    ]
    sentences = [sentence.split(" ") for sentence in raw_sentences]
    attn_weights = [softmax(np.random.random((len(s),len(s))) * 50, axis=1)
                    for s in sentences]
    dummy_data = {
        "raw_sentences": raw_sentences,
        "sentences": sentences,
        "attn_weights": attn_weights,
    }
    return dummy_data

def get_elements(params):
    element_list = []
    current_sample_ix = params['current_sample_ix']

    words = params["sentences"][current_sample_ix]
    wordmap = get_wordmap(words)
    element_list += wordmap 

    return element_list

def get_spans(params):
    sentence_ix = params['current_sample_ix']
    selected_word_ix = params['selected_word_ix']

    sentence = params['sentences'][sentence_ix]
    attn_weights = params['attn_weights'][sentence_ix]

    if not selected_word_ix: # need not be selected
        attn = np.ones(len(sentence))
    else:
        attn = [attn_weights[selected_word_ix][i] \
            if i != selected_word_ix else 1. \
            for i in range(len(sentence))]

    # set minimum opacity
    opacity = np.array(attn)
    opacity[opacity < .2] = .2

    spans = []
    tooltips = []
    for i,s in enumerate(sentence):
        display = s + " "
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


# re-render?
@app.callback(
    Output("display","children"),
    Input("explorer-view-store","data"))
def displayer(data):
    return data['selected_word_ix']

@app.callback(
    Output("span-holder","children"),
    Input("explorer-view-store","data"))
def span_update(params):
    if not params:
        return
    new_spans, new_tooltips = get_spans(params)
    return new_spans + new_tooltips

def get_layout():
    params = {
        "current_sample_ix": 0,
        "selected_word_ix": 0,
        "current_head": 0,
        "n_heads": 4
    }
    params.update(get_dummy_data(params))

    current_sample_ix = params['current_sample_ix']
    sentence = params['sentences'][current_sample_ix]

    paragraph = html.P(" ".join(sentence))
    
    rows = len(sentence) // WORDS_PER_ROW
    cyto_layout = get_cyto_layout(params, n_rows=rows)

    spans, tooltips = get_spans(params)
    spans += tooltips # roll tolltips into layout

    layout = html.Div(
        [
            dcc.Store(id="explorer-view-store", data=params),
            html.H1("Attention"),
            paragraph,
            cyto_layout,
            html.P(id="span-holder",children=spans),
            html.P(id="display",children=params['selected_word_ix'])
        ]
    )

    return layout

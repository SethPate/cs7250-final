from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
import numpy as np
from scipy.special import softmax
import pickle

from pages.maindash import app
from . import intro
from . import sidebar
from .attn import attn
from . import ff
from . import embed
from . import decoder

"""
Experimental single scroll layout.
"""

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

def make_single_layout():
    """Pulls together all the content and structure pages."""

    # init params and grab data
    params = {
        "current_sample_ix": 0,
        "selected_word_ix": 0,
    }
    params.update(get_dummy_data(params))

    # make all the layouts and put em together
    loc = dcc.Location(id="url")
    sb = sidebar.sidebar_layout
    content = html.Div([
        intro.make_layout(),
        embed.make_layout(),
        attn.get_layout(params),
        ff.get_layout(),
        decoder.get_layout(),
        ])

    return html.Div([loc, sb, content])

# Test case to show the selection reactively
@app.callback(
    Output("display","children"),
    Input("datastore","data"))
def displayer(data):
    return data['selected_word_ix']

"""
Update the data to reflect a selected word from the cytoscape.
"""
@app.callback(
    Output("datastore", "data"),
    Input("attn-cyto", "selectedNodeData"),
    Input("attn-cyto", "mouseoverNodeData"),
    State("datastore", "data"))
def selectHelper(selections, mouseover, data):
    if selections:
        data['selected_word_ix'] = selections[0]['ix']
    elif mouseover:
        data['selected_word_ix'] = mouseover['ix']
    else:
        data['selected_word_ix'] = None

    return data
